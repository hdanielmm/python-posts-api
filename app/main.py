from fastapi import FastAPI

from routers import post, db_posts, orm_posts, users, auth, votes

from database.orm_config import engine
from models import ormpost as models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Routers
app.include_router(post.router)
app.include_router(db_posts.router)
app.include_router(orm_posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(votes.router)


@app.get("/")
def root():
    return {"message": "Welcome"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app", host="127.0.0.1", port=8000, log_level="info", reload=True
    )
