from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr
from pydantic.types import conint

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

    # class Config:
    #     orm_mode = True


class PostCreate(PostBase):
    pass


class UserBase(BaseModel):
    email: EmailStr

    # class Config:
    #     orm_mode = True


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    created_at: datetime
    # disabled: bool | None

    class Config:
        orm_mode = True


class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: User
    title: str
    content: str

    class Config:
        orm_mode = True

class PostVote(PostBase):
    post: list[Post] = []
    votes: int

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None


class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)
