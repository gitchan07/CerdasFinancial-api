from models.base import Base
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

import bcrypt
from db import db

class Users(db.Model):
    __tablename__ = 'users'
    id = Column(String(36), primary_key=True)
    email = Column(String(100), nullable=False)
    password = Column(String(100), nullable=False)
    full_name = Column(String(100), nullable=False)
    is_subscribe = Column(Integer, default=0)
    subscribe_time = Column(DateTime, default=None)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    watchlists = relationship("Watchlist", backref="Users", lazy=True)
    subscribe = relationship("Subscribe", backref="Users", lazy=True)
    courses = relationship("Course", backref="Users", lazy=True)

    def set_password(self, password):
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))

