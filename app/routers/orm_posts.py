from typing import List
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException, Response, status

from app.database.orm_config import engine, get_db
from sqlalchemy.orm import Session
from app.models import ormpost as models
from app.models.schemas import Post, PostCreate

models.Base.metadata.create_all(bind=engine)

router = APIRouter(prefix="/orm-posts", tags=["orm"])


class Error404(Exception):
    pass


def error_404(id: int):
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Post with id: {id} was not found",
    )


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[Post])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.OrmPost).all()

    return posts


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=Post)
def get_post_by_id(id: int, db: Session = Depends(get_db)):
    # post = db.query(models.OrmPost).filter_by(id=id).first()
    post = db.query(models.OrmPost).filter(models.OrmPost.id == id).first()

    return post


@router.post("/", response_model=Post)
def create_posts(post: PostCreate, db: Session = Depends(get_db)):
    # new_post = models.OrmPost(
    #     title=post.title, content=post.content, published=post.published
    # )

    new_post = models.OrmPost(**post.dict())

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post

@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_post(id: int, db: Session = Depends(get_db)):
    try:
        post = db.query(models.OrmPost).filter(models.OrmPost.id == id)
        
        if post.first() is None:
            raise Error404()
        
        post.delete(synchronize_session=False)
        db.commit()

        return Response(status_code=status.HTTP_200_OK)
    except Error404:
        raise error_404(id)
    except Exception as e:
        print("Error: %s" % e)

@router.put("/{id}", response_model=Post)
def update_post(id: str, post: PostCreate, db: Session = Depends(get_db)):
    try:
        post_query = db.query(models.OrmPost).filter(models.OrmPost.id == id)

        if post_query.first() is None:
            raise Error404()
        # post_query.update({"title": "updated title", "content": "updated content", "published": True}, sinchronized_session=False)
        # post_query.update({"title": post.title, "content": post.content, "published": post.published}, synchronize_session=False)
        post_query.update(post.dict(), synchronize_session=False)

        db.commit()

        return post_query.first()
    except Error404:
        raise error_404(id)
    except Exception as e:
        print("Error: %s" % e)