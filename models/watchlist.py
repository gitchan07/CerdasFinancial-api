from models.base import Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from db import db

class Watchlist(Base):
    __tablename__ = 'watchlist'
    
    id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey('users.id'), nullable=False)
    course_id = Column(String, ForeignKey('courses.id'), nullable=False)
    
    user = relationship("User", back_populates="watchlists")
    course = relationship("Course", back_populates="watchlists")
