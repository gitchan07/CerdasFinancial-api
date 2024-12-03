from models.base import Base
from db import db
from sqlalchemy import Column, String, ForeignKey

class CourseCategory(db.Model):
    __tablename__ = 'courses_category'
    id = Column(String(36), primary_key=True)
    course_id = Column(String(36), ForeignKey('courses.id'), nullable=False)
    category_id = Column(String(36), ForeignKey('category.id'), nullable=False)