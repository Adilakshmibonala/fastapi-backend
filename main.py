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
