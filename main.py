from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class BlogDetails(BaseModel):
    name: str
    user_id: int


@app.get(path="/")
def index():
    return {
        "data": {
            "name": "AdiLakshmi"
        }
    }


@app.get("/about")
def about():
    return {
        "data": {
            "I am a backend developer."
        }
    }


@app.get('/about/{id_number}')
def blog_details(id_number: int):
    return {
        "data": id_number
    }


@app.get('/about/{id_number}/comments')
def blog_details(id_number):
    return {
        "data": {
            "comments": id_number
        }
    }


@app.get('/query')
def blog_details(limit: int, offset: int):
    return {
        "data": {
            "limit": limit,
            "offset": offset
        }
    }


@app.post(path="/blog")
def create_blog(blog: BlogDetails):
    return {
        "data": {
            "blog_details": {
                "name": blog.name,
                "user_id": blog.user_id
            }
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=9000)
