from fastapi import APIRouter, Depends, HTTPException, Query
from datetime import date
from sqlalchemy.orm import Session
from typing import List

from app.schemas.lesson import Lesson, LessonForTeacherCallender, LessonUpdate, LessonExtended
from app.crud import crud_lesson
from app.api import deps

router = APIRouter()

@router.get("/", response_model=list[LessonForTeacherCallender])
def get_lessons_for_teacher(
    db: Session = Depends(deps.get_db),
    current_teacher=Depends(deps.get_current_teacher),
    start_date: date = Query(None),
    end_date: date = Query(None),
):
    lessons = crud_lesson.get_lessons_for_teacher(db, teacher_id=current_teacher.id, start_date=start_date, end_date=end_date)
    return [
        LessonForTeacherCallender(
            id=lesson.id,
            date=lesson.date,
            start_time=lesson.start_time,
            end_time=lesson.end_time,
            student_id=lesson.student_id,
            student_first_name=lesson.student.first_name,
            student_last_name=lesson.student.last_name,
        )
        for lesson in lessons
    ]
    
@router.get("/unpaid", response_model=list[Lesson])
def get_unpaid_lessons(
    db: Session = Depends(deps.get_db),
    current_teacher=Depends(deps.get_current_teacher),
    student_id: int = Query(None),
    start_date: date = Query(None),
    end_date: date = Query(None)
):
    lessons = crud_lesson.get_lessons_for_teacher(db, teacher_id=current_teacher.id, student_id=student_id, start_date=start_date, end_date=end_date, unpaid=True)
    return lessons

@router.patch("/{lesson_id}", response_model=Lesson)
def update_lesson(
    lesson_id: int,
    lesson_in: LessonUpdate,
    db: Session = Depends(deps.get_db),
    current_teacher = Depends(deps.get_current_teacher),
):
    try:
        lesson = crud_lesson.get_lesson_by_id(db, lesson_id)
        if not lesson or lesson.teacher_id != current_teacher.id:
            raise HTTPException(status_code=404, detail="Lesson not found")
        updated = crud_lesson.update_lesson(db, lesson, lesson_in)
        return updated
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{lesson_id}", response_model=LessonExtended)
def get_lesson_by_id(
    *,
    db: Session = Depends(deps.get_db),
    current_teacher = Depends(deps.get_current_teacher),
    lesson_id: int
):
    lesson = crud_lesson.get_lesson_by_id(db, int(lesson_id), teacher_id=current_teacher.id, extended=True)
    if not lesson or lesson.teacher_id != current_teacher.id:
        raise HTTPException(status_code=404, detail="Lesson not found")
    print(lesson)
    return LessonExtended(
        id=lesson.id,
        topic=lesson.topic,
        date=lesson.date,
        start_time=lesson.start_time,
        end_time=lesson.end_time,
        notes=lesson.notes,
        price=lesson.price,
        paid_amount=lesson.paid_amount,
        student_id=lesson.student_id,
        student_first_name=lesson.student.first_name,
        student_last_name=lesson.student.last_name,
        student_email=lesson.student.email
    )