from fastapi import FastAPI, Depends, status, Response, HTTPException
from sqlalchemy.orm import Session
from . import schemas, models
from .database import engine, SessionLocal

app = FastAPI()

models.Base.metadata.create_all(engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/blog", status_code=status.HTTP_201_CREATED)
def create(request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.get("/blog/{id}", status_code=status.HTTP_200_OK)
def show(id: int, response: Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    # if not blog:
    #     response.status = status.HTTP_404_NOT_FOUND
    #     return {"blog not found"}
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="not found")
    return blog


@app.delete("/blog/{id}", status_code=status.HTTP_200_OK)
def delete(id: int, response: Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    db.delete(blog)
    db.commit()
    return "deleted"


@app.put(
    "/blog/{id}", response_model=schemas.ShowBlog, status_code=status.HTTP_202_ACCEPTED
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
