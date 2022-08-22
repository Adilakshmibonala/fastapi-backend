from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from post.auth.jwt_bearer import JwtBearer
from post.database import engine
from post import models
from post.schemas import Blog, UserSchema
from post.auth.jwt_handler import get_jwt_token

app = FastAPI()
models.Base.metadata.create_all(bind=engine)


def get_db():
    from post.database import SessionLocal

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post(path="/blog", dependencies=[Depends(JwtBearer())])
def create_blog(blog: Blog, db: Session = Depends(get_db)):
    new_blog = models.BlogDetails(name=blog.title, body=blog.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return {
        "data": new_blog
    }


@app.post(path="/user/login")
def user_login(user: UserSchema, db: Session = Depends(get_db)):
    from fastapi import HTTPException
    if db.query(models.User).filter(models.User.email==user.email, models.User.password==user.password):
        return get_jwt_token(email=user.email)
    else:
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
