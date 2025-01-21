from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from db import db


class SubscribeType(db.Model):
    __tablename__ = 'subscribe_type'
    id = Column(String(36), primary_key=True)
    duration = Column(Integer, nullable=False)
    price = Column(Integer, nullable=False)


