from pydantic import BaseModel
from typing import Optional


class Blog(BaseModel):
    title: str
    body: str


class ShowBlog(BaseModel):
    title: str
    body: str

    class Config:
        orm_mode = True


class UpdateBlog(BaseModel):
    title: Optional[str] = None
    body: Optional[str] = None
