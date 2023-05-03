from fastapi import FastAPI

from app.routers import post, db_posts, orm_posts, users, auth

from app.database.orm_config import engine
from app.models import ormpost as models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Routers
app.include_router(post.router)
app.include_router(db_posts.router)
app.include_router(orm_posts.router)
app.include_router(users.router)
app.include_router(auth.router)


@app.get("/")
def root():
    return {"message": "Welcome"}


# if "__name__" == "__main__":
#     import uvicorn

#     uvicorn.run(
#         "app.main:app", host="127.0.0.1", port="8000", log_level="info", reload=True
#     )
