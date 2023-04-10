from dotenv import load_dotenv
from fastapi import FastAPI

from app.routers import post, db_posts

app = FastAPI()

# Routers
app.include_router(post.router)
app.include_router(db_posts.router)

@app.get("/")
def root():
    return {"message": "Welcome"}
