from typing import Optional
from pydantic import BaseModel


class Post(BaseModel):
    title: str
    content: str
    published: Optional[bool] = True