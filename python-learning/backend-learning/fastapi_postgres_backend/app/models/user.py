from sqlalchemy import Column, Integer, String
from app.models.db_base import DBBaseModel

class User(DBBaseModel):
    __tablename__ = "users"
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
