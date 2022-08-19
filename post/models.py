from .database import Base
from sqlalchemy import Column, Integer, String


class BlogDetails(Base):
    __tablename__ = "Blog"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    body = Column(String)
