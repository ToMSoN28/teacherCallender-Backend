from pydantic import BaseModel
from typing import Optional, List
from datetime import date
from app.schemas.lesson import DecimalType


class LessonSerieBase(BaseModel):
    name: Optional[str] = None
    student_id: int
    teacher_id: int
    start_date: date
    end_date: date
    weekday: int  # 0=Monday, 6=Sunday
    start_time: str  # "HH:MM"
    end_time: str    # "HH:MM"
    price: Optional[DecimalType] = 0.00
    notes: Optional[str] = None

class LessonSerieCreate(LessonSerieBase):
    pass

class LessonSerie(LessonSerieBase):
    id: int

    class Config:
        from_attributes = True