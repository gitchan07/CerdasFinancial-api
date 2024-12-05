from models.courses import Course
from db import db
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

class ContentCourses(db.Model):
    __tablename__ = "content_course"
    id = Column(String(36), primary_key=True)
    content_list = Column(Integer, nullable=False)
    name = Column(String(200), nullable=False)
    description = Column(String(200), nullable=False)
    course_id = Column(String(36), ForeignKey('courses.id'), nullable=False)
    video_url = Column(String(100), nullable=False)

    course = relationship("Course", back_populates="content_courses") 

