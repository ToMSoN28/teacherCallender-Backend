# app/schemas/lesson.py
from pydantic import BaseModel, condecimal, EmailStr
from datetime import date, datetime
from typing import Optional

DecimalType = condecimal(max_digits=10, decimal_places=2)

class LessonBase(BaseModel):
    topic: str
    date: date
    start_time: datetime
    end_time: datetime
    notes: Optional[str] = None
    price: DecimalType
    paid_amount: DecimalType


class LessonCreate(LessonBase):
    pass

class Lesson(LessonBase):
    id: int
    student_id: int
    teacher_id: int

    class Config:
        from_attributes = True
        
class LessonForTeacherCallender(BaseModel):
    id: int
    date: date
    start_time: datetime
    end_time: datetime
    student_id: int
    student_first_name: str
    student_last_name: str

class LessonUpdate(BaseModel):
    topic: Optional[str] = None
    date: Optional[date] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    notes: Optional[str] = None
    price: Optional[DecimalType] = None
    paid_amount: Optional[DecimalType] = None
    
    
class LessonExtended(BaseModel):
    id: int
    topic: str
    date: date
    start_time: datetime
    end_time: datetime
    notes: Optional[str] = None
    price: DecimalType
    paid_amount: DecimalType
    student_id: int
    student_first_name: str
    student_last_name: str
    student_email: Optional[EmailStr] = None