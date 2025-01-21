from models.base import Base
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from db import db

class Subscribe(db.Model):
    __tablename__ = 'history_subscribe'
    id = Column(String(200), primary_key=True)
    user_id = Column(String(200), ForeignKey('users.id'), nullable=False)
    subscribe_date = Column(DateTime(timezone=True), server_default=func.now())
    subscribe_id = Column(String(36))
    transaction_date = Column(DateTime(timezone=True), server_default=func.now())
    status_payment = Column(String(36), nullable=False, default=0)
    payment_method = Column(String(36), nullable=False, default=0)
    account_no = Column(String(200), nullable=True)
    currency = Column(String(36), nullable=True)

