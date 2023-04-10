from app.posts_db.post_data import my_posts
from app.models.post import Post
from fastapi import APIRouter, HTTPException, Response, status
from random import randrange

router = APIRouter(prefix="/posts", tags=["mock db"])


def search_post(id: str):
    posts = filter(lambda post: post["id"] == id, my_posts)
    try:
        return list(posts)[0]
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} was not found",
        )


def search_index(id: str):
    for index, post in enumerate(my_posts):
        if post["id"] == id:
            return index


@router.get("/")
def get_posts():
    return {"posts": my_posts}


@router.post("/new_post", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    id = randrange(1, 100000000000)

    post_dict = dict(post)
    # print(f"post_dict {post_dict['id']}")
    post_dict["id"] = str(id)

    my_posts.append(post_dict)

    return {"post_details": post_dict}


@router.get("/latest_post")
def get_latest_post():
    return {"post_details": my_posts[-1]}


@router.get("/{id}")
def get_post_by_id(id: str):
    post = search_post(id)
    return {"post_details": post}


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: str):
    index = search_index(id)

    if index is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} does not exist",
        )

    del my_posts[index]

    return Response(
        status_code=status.HTTP_204_NO_CONTENT
    )  # {"message": "Post deleted successfully"}


@router.put("/{id}")
def put_post(id: str, post: Post):
    index = search_index(id)

    if index is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} does not exist",
        )

    post_dict = post.dict()
    post_dict["id"] = id
    my_posts[index] = post_dict

    return {"post details": my_posts[index]}
