from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.base import Base

class Teacher(Base):
    __tablename__ = "teachers"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    students = relationship("Student", back_populates="teacher")
    lessons = relationship("Lesson", back_populates="teacher", cascade="all, delete-orphan")
    lesson_series = relationship("LessonSerie", back_populates="teacher", cascade="all, delete-orphan")