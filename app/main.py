from dotenv import load_dotenv
from fastapi import Depends, FastAPI

from app.routers import post, db_posts, orm_posts, users

from app.database.orm_config import engine, get_db
from app.models import ormpost as models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Routers
app.include_router(post.router)
app.include_router(db_posts.router)
app.include_router(orm_posts.router)
app.include_router(users.router)


@app.get("/")
def root():
    return {"message": "Welcome"}
