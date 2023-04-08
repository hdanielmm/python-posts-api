from fastapi import FastAPI
from app.routers import post

app = FastAPI()

# Routers
app.include_router(post.router)

@app.get('/')
def root():
    return {'message': 'Welcome'}