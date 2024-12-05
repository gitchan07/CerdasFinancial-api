from models.base import Base
from sqlalchemy import Column, String, Text, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from db import db

class Course(db.Model):
    __tablename__ = 'courses'
    
    id = Column(String(36), primary_key=True)  
    name = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    detail = Column(Text, nullable=True)
    video_url = Column(String(200), nullable=True)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    created_by = Column(String(200), ForeignKey('users.id'), nullable=True) 
    
    watchlists = relationship("Watchlist", back_populates="course")
    categories = relationship("CourseCategory", back_populates="course")
    content_courses = relationship("ContentCourses", back_populates="course")


