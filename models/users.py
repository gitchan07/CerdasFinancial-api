from models.base import Base
from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.sql import func
import bcrypt

class Users(Base):
    __tablename__ = 'users'
    id = Column(String, primary_key=True)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    is_subscribe = Column(Integer, default=0)
    subscribe_time = Column(DateTime, default=None)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at =Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    def set_password(self, password):
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))