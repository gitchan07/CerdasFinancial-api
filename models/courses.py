from models.base import Base
from sqlalchemy import Column, String, Text, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

class Course(Base):
    __tablename__ = 'courses'
    
    id = Column(String, primary_key=True)  
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    detail = Column(Text, nullable=True)
    video_url = Column(String, nullable=True)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    created_by = Column(String, ForeignKey('users.id'), nullable=False) 
    
    watchlist = relationship("Watchlist", back_populates="course")
    contents = relationship("ContentsCourse", back_populates="course") 
    categories = relationship("CoursesCategory", back_populates="course")
