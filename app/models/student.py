# app/models/student.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True, nullable=False)
    last_name = Column(String, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=True)
    teacher_id = Column(Integer, ForeignKey("teachers.id"))
    teacher = relationship("Teacher", back_populates="students")
    lessons = relationship("Lesson", back_populates="student", cascade="all, delete-orphan")
    lesson_series = relationship("LessonSerie", back_populates="student", cascade="all, delete-orphan")