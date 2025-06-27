# app/api/v1/endpoints/students.py
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.schemas.student import Student, StudentCreate
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
