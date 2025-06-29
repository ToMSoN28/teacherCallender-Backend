# app/api/v1/endpoints/students.py
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from datetime import date

from app.schemas.student import Student, StudentCreate
from app.schemas.lesson import Lesson, LessonCreate
from app.crud import crud_lesson
from app.crud import crud_student
from app import crud, models
from app.api import deps

router = APIRouter()

@router.post("/", response_model=Student)
def create_student(
    *,
    db: Session = Depends(deps.get_db),
    current_teacher = Depends(deps.get_current_teacher),
    student_in: StudentCreate,
):
    """
    Tworzy nowego studenta.
    """
    student = crud_student.create_student(db=db, teacher_id=current_teacher.id, student=student_in)
    return student

@router.get("/", response_model=List[Student])
def read_students(
    db: Session = Depends(deps.get_db),
    current_teacher = Depends(deps.get_current_teacher),
    skip: int = 0,
    limit: int = 100,
):
    """
    Pobiera listę studentów.
    """
    students = crud_student.get_students(db, teacher_id=current_teacher.id, skip=skip, limit=limit)
    return students

@router.get("/{student_id}", response_model=Student)
def read_student(
    *,
    db: Session = Depends(deps.get_db),
    current_teacher = Depends(deps.get_current_teacher),
    student_id: int,
):
    """
    Pobiera studenta po ID.
    """
    student = crud_student.get_student(db=db, teacher_id=current_teacher.id, student_id=student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

@router.get("/{student_id}/lessons", response_model=List[Lesson])
def read_lessons(
    student_id: int,
    db: Session = Depends(deps.get_db),
    current_teacher = Depends(deps.get_current_teacher),
    start_date: date = Query(None),
    end_date: date = Query(None),
):
    lessons = crud_lesson.get_lessons_by_student(db, student_id=student_id, teacher_id=current_teacher.id, start_date=start_date, end_date=end_date)
    return lessons

@router.post("/{student_id}/lessons", response_model=Lesson)
def create_lesson(
    student_id: int,
    lesson_in: LessonCreate,
    db: Session = Depends(deps.get_db),
    current_teacher = Depends(deps.get_current_teacher),
):
    try:
        lesson = crud_lesson.create_lesson_for_student(
            db, student_id=student_id, teacher_id=current_teacher.id, lesson_in=lesson_in
        )
        return lesson
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
