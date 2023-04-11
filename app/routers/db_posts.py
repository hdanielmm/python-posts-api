import os
import psycopg2
import time
from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException, Response, status
from psycopg2.extras import RealDictCursor

from app.models.post import Post


router = APIRouter(prefix="/db-posts", tags=["postgresql"])


load_dotenv()

user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")


class Error404(Exception):
    pass


while True:
    try:
        conn = psycopg2.connect(
            host="127.0.0.1",
            database="fastapi-youtube",
            user=user,
            password=password,
            cursor_factory=RealDictCursor,
        )
        cursor = conn.cursor()
        print("Database connection was established")
        break
    except Exception as error:
        print("Error connecting to database")
        print("Error: ", error)
        time.sleep(2)


def error_404(id: str):
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Post with id: {id} was not found",
    )


@router.get("/")
def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()

    return {"posts": posts}


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    cursor.execute(
        """INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""",
        (post.title, post.content, post.published),
    )

    new_post = cursor.fetchone()
    conn.commit()

    return {"message": "Post created successfully", "post details": new_post}


@router.get("/{id}")
def get_post_by_id(id: str):
    try:
        cursor.execute("""SELECT * FROM posts WHERE id = %s""" % str(id))
        # cursor.execute("""SELECT * FROM posts WHERE id = %s""", str(id))

        post = cursor.fetchone()
        print(f"Post {post}")
        if post is None:
            raise Error404()

        return {"post details": post}
    except Error404:
        raise error_404(id)
    except Exception as e:
        print("Error: %s" % e)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: str):
    try:
        cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""" % id)
        deleted_post = cursor.fetchone()

        if deleted_post is None:
            print("Response0")
            raise Error404()

        conn.commit()
        print("Response1")

        return Response(
            status_code=status.HTTP_204_NO_CONTENT
        )  # {"message": "Post deleted successfully"}
    except Error404:
        raise error_404(id)
    except Exception as e:
        print("Exception: %s" % (e))


@router.put("/{id}")
def put_post(id: str, post: Post):
    try:
        cursor.execute(
            """UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
            (post.title, post.content, post.published, id)
        )

        updated_post = cursor.fetchone()

        if updated_post is None:
            raise Error404()

        conn.commit()
        return Response(content="Post updated successfully", status_code=status.HTTP_200_OK)
    except Error404:
        raise error_404(id)
    except Exception as e:
        print("Exception: %s" % e)
