from typing import List
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException, Response, status

from app.database.orm_config import get_db
from sqlalchemy.orm import Session
from app.models import ormpost as models
from app.models.schemas import Post, PostCreate
from .. import oauth2


router = APIRouter(prefix="/orm-posts", tags=["orm"])


class Error404(Exception):
    pass


def error_404(id: int):
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Post with id: {id} was not found",
    )


# Verify that the current user is the author of the post
def verify_author_post(owner_id: int, current_user_id: int):
    if owner_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action",
        )

    print("Everything is fine")


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[Post])
def get_posts(
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
    limit: int = 5,
    skip: int = 0,
    search: str | None = "",
):
    # posts = db.query(models.OrmPost).all()
    # de
    posts = (
        db.query(models.OrmPost)
        .filter(
            models.OrmPost.owner_id == current_user.id,
            models.OrmPost.title.contains(search),
        )  # Brings out the owner posts
        .limit(limit)
        .offset(skip)
        .all()
    )

    return posts


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=Post)
def get_post_by_id(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    # post = db.query(models.OrmPost).filter_by(id=id).first()
    post = db.query(models.OrmPost).filter(models.OrmPost.id == id).first()

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found"
        )

    verify_author_post(post.owner_id, current_user.id)

    return post


@router.post("/", response_model=Post)
def create_posts(
    post: PostCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    # new_post = models.OrmPost(
    #     title=post.title, content=post.content, published=post.published
    # )

    new_post = models.OrmPost(owner_id=current_user.id, **post.dict())

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    try:
        post_query = db.query(models.OrmPost).filter(models.OrmPost.id == id)
        post = post_query.first()

        if post is None:
            raise Error404()

        verify_author_post(post.owner_id, current_user.id)

        post_query.delete(synchronize_session=False)
        db.commit()

        return Response(status_code=status.HTTP_200_OK)
    except Error404:
        raise error_404(id)
    except Exception as e:
        print("Error: %s" % e)


@router.put("/{id}", response_model=Post)
def update_post(
    id: str,
    post: PostCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    try:
        post_query = db.query(models.OrmPost).filter(models.OrmPost.id == id)

        if post_query.first() is None:
            raise Error404()

        verify_author_post(post_query.first().owner_id, current_user.id)

        # post_query.update({"title": "updated title", "content": "updated content", "published": True}, sinchronized_session=False)
        # post_query.update({"title": post.title, "content": post.content, "published": post.published}, synchronize_session=False)
        post_query.update(post.dict(), synchronize_session=False)

        db.commit()

        return post_query.first()
    except Error404:
        raise error_404(id)
    except Exception as e:
        print("Error: %s" % e)
