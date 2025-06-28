# app/models/lesson.py
from sqlalchemy import Column, Integer, String, ForeignKey, Date, DateTime, Text, Numeric
from sqlalchemy.orm import relationship
from app.db.base import Base

class Lesson(Base):
    __tablename__ = "lessons"

    id = Column(Integer, primary_key=True, index=True)
    topic = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    notes = Column(Text, nullable=True)
    price = Column(Numeric(10, 2), nullable=False)        # Kwota do zapłaty
    paid_amount = Column(Numeric(10, 2), nullable=False)  # Ile wpłacono
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    teacher_id = Column(Integer, ForeignKey("teachers.id"), nullable=False)

    student = relationship("Student", back_populates="lessons")
    teacher = relationship("Teacher", back_populates="lessons")