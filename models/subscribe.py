from models.base import Base
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.sql import func

class Subscribe(Base):
    __tablename__ = 'history_subscribe'
    id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey('users.id'), nullable=False)
    subscribe_date = Column(DateTime(timezone=True), server_default=func.now())
    price =  Column(Integer)
