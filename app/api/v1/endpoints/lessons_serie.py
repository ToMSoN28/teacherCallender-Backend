from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.schemas.lesson_serie import LessonSerie, LessonSerieCreate
from app.crud import crud_lesson
from app.models.lesson_serie import LessonSerie as LessonSerieModel
from app.schemas.lesson import Lesson
from app.api import deps

router = APIRouter()

@router.post("/", response_model=LessonSerie)
def create_serie(
    serie_in: LessonSerieCreate,
    db: Session = Depends(deps.get_db),
    current_teacher = Depends(deps.get_current_teacher),
):
    return crud_lesson.create_lesson_serie(db, serie_in, teacher_id=current_teacher.id)

@router.get("/", response_model=List[LessonSerie])
def get_all_series(
    db: Session = Depends(deps.get_db),
    current_teacher = Depends(deps.get_current_teacher),
):
    return db.query(LessonSerieModel).filter(LessonSerieModel.teacher_id == current_teacher.id).all()

@router.get("/{serie_id}", response_model=LessonSerie)
def get_serie(
    serie_id: int,
    db: Session = Depends(deps.get_db),
    current_teacher = Depends(deps.get_current_teacher),
):
    serie = db.query(LessonSerieModel).filter(
        LessonSerieModel.id == serie_id,
        LessonSerieModel.teacher_id == current_teacher.id
    ).first()
    if not serie:
        raise HTTPException(status_code=404, detail="Lesson serie not found")
    return serie

@router.get("/{serie_id}/lessons", response_model=List[Lesson])
def get_serie_lessons(
    serie_id: int,
    db: Session = Depends(deps.get_db),
    current_teacher = Depends(deps.get_current_teacher),
):
    lessons = crud_lesson.get_lessons_for_serie(db, serie_id=serie_id, teacher_id=current_teacher.id)
    return lessons