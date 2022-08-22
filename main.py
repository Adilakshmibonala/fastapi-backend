from sqlalchemy.orm import Session
from post.database import engine
from post import models
from post.schemas import Blog, UserSchema
from decouple import config
from fastapi import FastAPI, HTTPException, Depends
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import MissingTokenError
from pydantic import BaseModel


app = FastAPI()
models.Base.metadata.create_all(bind=engine)


class Settings(BaseModel):
    authjwt_secret_key: str = config("JWT_SECRET_KEY")


@AuthJWT.load_config
def get_config():
    return Settings()


def get_db():
    from post.database import SessionLocal

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post(path="/blog")
def create_blog(blog: Blog, authorize: AuthJWT = Depends()):
    try:
        authorize.jwt_required()
    except MissingTokenError:
        raise HTTPException(status_code=403, detail="Access Denied")
    # new_blog = models.BlogDetails(name=blog.title, body=blog.body)
    # db.add(new_blog)
    # db.commit()
    # db.refresh(new_blog)
    current_user = authorize.get_jwt_subject()
    return {
        "data": current_user
    }


@app.post(path="/user/login")
def user_login(user: UserSchema, authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    from fastapi import HTTPException

    user_obj = db.query(models.User).filter(
        models.User.email == user.email, models.User.password == user.password).first()
    if user_obj:
        access_token = authorize.create_access_token(subject=user_obj.email)
        refresh_token = authorize.create_refresh_token(subject=user_obj.email)

        return {"access_token": access_token, "refresh_token": refresh_token}
    raise HTTPException(status_code=403, detail="Unauthorised User")


@app.post(path="/user/signup")
def user_signup(user: UserSchema, db: Session = Depends(get_db)):
    new_user = models.User(email=user.email, password=user.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "data": new_user
    }


@app.post('/refresh')
def refresh(authorize: AuthJWT = Depends()):
    try:
        authorize.jwt_refresh_token_required()
    except MissingTokenError:
        raise HTTPException(status_code=400, detail="Request Token Required")

    current_user = authorize.get_jwt_subject()
    new_access_token = authorize.create_access_token(subject=current_user)
    return {"access_token": new_access_token}
