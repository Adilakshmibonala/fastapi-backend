from fastapi import FastAPI
from post.schemas import Blog

app = FastAPI()


@app.post(path="/blog")
def create(blog: Blog):
    return {
        "title": blog.title,
        "body": blog.body
    }
