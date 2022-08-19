from fastapi import FastAPI

app = FastAPI()


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

