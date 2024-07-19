from fastapi import FastAPI, Depends, status, Response, HTTPException
from sqlalchemy.orm import Session
from . import schemas, models
from .database import engine, SessionLocal
from .hashing import hash
from typing import List

app = FastAPI()

models.Base.metadata.create_all(engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get(
    "/blog",
    status_code=status.HTTP_200_OK,
    response_model=List[schemas.ShowBlog],
    tags=["Blog"],
)
def all(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


@app.post("/blog", status_code=status.HTTP_201_CREATED, tags=["Blog"])
def create(request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.get("/blog/{id}", status_code=status.HTTP_200_OK, tags=["Blog"])
def show(id: int, response: Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    # if not blog:
    #     response.status = status.HTTP_404_NOT_FOUND
    #     return {"blog not found"}
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="not found")
    return blog


@app.delete("/blog/{id}", status_code=status.HTTP_200_OK, tags=["Blog"])
def delete(id: int, response: Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    db.delete(blog)
    db.commit()
    return "deleted"


@app.put(
    "/blog/{id}",
    response_model=schemas.ShowBlog,
    status_code=status.HTTP_202_ACCEPTED,
    tags=["Blog"],
)
def update(id: int, request: schemas.UpdateBlog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found"
        )

    if request.title is not None:
        blog.title = request.title
    if request.body is not None:
        blog.body = request.body

    if request.title is None and request.body is None:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT, detail="not content"
        )

    db.commit()
    db.refresh(blog)
    return blog


@app.post(
    "/users",
    status_code=status.HTTP_201_CREATED,
    tags=["users"],
)
def create_user(request: schemas.Users, db: Session = Depends(get_db)):
    hashed_password = hash.bcrypt(request.password)
    new_user = models.Users(
        name=request.name, email=request.email, password=hashed_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.get(
    "/users/{id}", status_code=status.HTTP_200_OK, response_model=schemas.ShowUsers
)
def show_users(id: int, response: Response, db: Session = Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="user id not found"
        )
    return user
