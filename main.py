from fastapi import FastAPI

app = FastAPI()


def index():
    return "Hello Adi"
