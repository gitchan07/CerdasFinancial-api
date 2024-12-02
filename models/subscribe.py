from models.base import Base
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.sql import func
from db import db

class Subscribe(db.Model):
    __tablename__ = 'history_subscribe'
    id = db.Column(db.tring, primary_key=True)
    user_id = db.Column(db.String, ForeignKey('users.id'), nullable=False)
    subscribe_date = db.Column(db.DateTime(timezone=True), server_default=func.now())
    price =  db.Column(db.Integer)
