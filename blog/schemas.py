from pydantic import BaseModel
from typing import Optional


class Blog(BaseModel):
    title: str
    body: str


class ShowBlog(BaseModel):
    title: str
    body: str

    class Config:
        from_attributes = True


class UpdateBlog(BaseModel):
    title: Optional[str] = None
    body: Optional[str] = None


class Users(BaseModel):
    name: str
    email: str
    password: str


class ShowUsers(BaseModel):
    name: str
    email: str
    password: str

    class Config:
        from_attributes = True
