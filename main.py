from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from post.database import engine
from post.schemas import Blog
from post import models

app = FastAPI()


models.Base.metadata.create_all(bind=engine)


def get_db():
    from post.database import SessionLocal

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post(path="/blog")
def create(blog: Blog, db: Session = Depends(get_db)):
    return {
        "title": blog.title,
        "body": blog.body
    }
