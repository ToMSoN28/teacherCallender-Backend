from sqlalchemy import Column, Integer, String, ForeignKey, Date, DateTime, Text, Numeric
from sqlalchemy.orm import relationship
from app.db.base import Base

class LessonSerie(Base):
    __tablename__ = "lesson_series"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    teacher_id = Column(Integer, ForeignKey("teachers.id"), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    weekday = Column(Integer, nullable=False)  # 0=Monday, 6=Sunday
    start_time = Column(String, nullable=False)  # "HH:MM"
    end_time = Column(String, nullable=False)    # "HH:MM"
    price = Column(Numeric(10, 2), nullable=False)
    notes = Column(Text, nullable=True)

    student = relationship("Student", back_populates="lesson_series")
    teacher = relationship("Teacher", back_populates="lesson_series")
    lessons = relationship("Lesson", back_populates="lesson_serie", cascade="all, delete-orphan")