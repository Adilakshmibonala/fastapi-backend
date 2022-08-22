from pydantic import BaseModel, Field, EmailStr


class Blog(BaseModel):
    title: str
    body: str


class UserSchema(BaseModel):
    email: EmailStr
    password: str
