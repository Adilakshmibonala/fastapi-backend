import datetime

from sqlalchemy.orm import Session
from post.database import engine
from post import models
from post.schemas import Blog, UserSchema
from decouple import config
from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import MissingTokenError
from pydantic import BaseModel
from fastapi.openapi.utils import get_openapi


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
    import bcrypt

    passwd_in_bytes = bytes(user.password, encoding="raw_unicode_escape")
    user_obj = db.query(models.User).filter(models.User.email == user.email).first()

    if user_obj and bcrypt.checkpw(passwd_in_bytes, user_obj.password):
        access_token = authorize.create_access_token(
            subject=user_obj.email, expires_time=datetime.timedelta(days=int(config("ACCESS_TOKEN_EXPIRES_IN_DAYS"))),
            algorithm=config("JWT_ALGORITHM"))
        refresh_token = authorize.create_refresh_token(
            subject=user_obj.email, expires_time=datetime.timedelta(days=int(config("REFRESH_TOKEN_EXPIRES_IN_DAYS"))),
            algorithm=config("JWT_ALGORITHM"))

        return {"access_token": access_token, "refresh_token": refresh_token}
    raise HTTPException(status_code=403, detail="Unauthorised User")


@app.post(path="/user/signup")
def user_signup(user: UserSchema, db: Session = Depends(get_db)):
    import bcrypt

    passwd_in_bytes = bytes(user.password, encoding="raw_unicode_escape")
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(passwd_in_bytes, salt)

    new_user = models.User(email=user.email, password=hashed_password)
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
    expires_time = datetime.timedelta(days=int(config("REFRESH_TOKEN_EXPIRES_IN_DAYS")))
    new_access_token = authorize.create_access_token(
        subject=current_user, expires_time=expires_time, algorithm=config("JWT_ALGORITH"))
    return {"access_token": new_access_token}


@app.get("/users")
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users


@app.get("/user/{user_id}")
def get_user_details(user_id, db: Session = Depends(get_db)):
    user_obj = db.query(models.User.id == user_id).first()
    return user_obj
