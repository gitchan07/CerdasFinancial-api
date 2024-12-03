from models.base import Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from db import db

class Watchlist(db.Model):
    __tablename__ = 'watchlist'
    
    id = Column(String(200), primary_key=True)
    user_id = Column(String(200), ForeignKey('users.id'), nullable=False)
    course_id = Column(String(200), ForeignKey('courses.id'), nullable=False)
    
    user = relationship("User", back_populates="watchlists")
    course = relationship("Course", back_populates="watchlists")
