import os
import psycopg2
import time
from dotenv import load_dotenv
from fastapi import APIRouter, status
from psycopg2.extras import RealDictCursor

from app.models.post import Post


router = APIRouter(prefix="/db-posts", tags=["postgresql"])


load_dotenv()

user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")

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
