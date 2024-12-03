from models.base import Base
from db import db
from sqlalchemy import Column, String

class Category(db.Model):
    __tablename__ = 'category'
    id = Column(String(200), primary_key=True)
    name = Column(String(200), nullable=False)
