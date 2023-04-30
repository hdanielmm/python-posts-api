from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr


class PostBase(BaseModel):
    title: str
    content: str
    published: Optional[bool] = True
    

    class Config:
        orm_mode = True


class PostCreate(PostBase):
    pass


class UserBase(BaseModel):
    email: EmailStr

    class Config:
        orm_mode = True


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    created_at: datetime
    disabled: bool | None


class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: User


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None