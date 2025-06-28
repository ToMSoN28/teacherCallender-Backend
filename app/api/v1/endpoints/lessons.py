from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.schemas.lesson import Lesson, LessonCreate
from app.crud import crud_lesson
from app.api import deps

router = APIRouter()

@router.get("/", response_model=List[Lesson])
def read_lessons(
    student_id: int,
    db: Session = Depends(deps.get_db),
    current_teacher = Depends(deps.get_current_teacher),
):
    lessons = crud_lesson.get_lessons_by_student(db, student_id=student_id, teacher_id=current_teacher.id)
    return lessons

@router.post("/", response_model=Lesson)
def create_lesson(
    student_id: int,
    lesson_in: LessonCreate,
    db: Session = Depends(deps.get_db),
    current_teacher = Depends(deps.get_current_teacher),
):
    lesson = crud_lesson.create_lesson_for_student(
        db, student_id=student_id, teacher_id=current_teacher.id, lesson_in=lesson_in
    )
    return lesson