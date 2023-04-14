from dotenv import load_dotenv
from fastapi import Depends, FastAPI

from app.routers import post, db_posts
from app.models import ormpost as models
from app.database.orm_config import engine, get_db

from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Routers
app.include_router(post.router)
app.include_router(db_posts.router)

@app.get("/")
def root():
    return {"message": "Welcome"}

@app.get("/sqlalchemy")
def test_sqlalchemy(db: Session = Depends(get_db)):
    return {"message": "Success"}
