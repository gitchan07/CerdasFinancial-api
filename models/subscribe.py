from models.base import Base
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.sql import func
from db import db

class Subscribe(db.Model):
    __tablename__ = 'history_subscribe'
    id = Column(String(200), primary_key=True)
    user_id = Column(String(200), ForeignKey('users.id'), nullable=False)
    subscribe_date = Column(DateTime(timezone=True), server_default=func.now())
    price =  Column(Integer)
