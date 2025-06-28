from sqlalchemy.orm import Session, joinedload
from app.models.lesson import Lesson
from app.schemas.lesson import LessonCreate
from datetime import date

def get_lessons_by_student(db: Session, student_id: int, teacher_id: int = None):
    return db.query(Lesson).filter(Lesson.student_id == student_id and teacher_id == teacher_id).all()

def get_lessons_for_teacher(db: Session, teacher_id: int, start_date: date = None, end_date: date = None):
    query = db.query(Lesson).options(joinedload(Lesson.student)).filter(Lesson.teacher_id == teacher_id)
    if start_date:
        query = query.filter(Lesson.date >= start_date)
    if end_date:
        query = query.filter(Lesson.date <= end_date)
    return query.all()

def get_unpaid_lessons(db: Session, teacher_id: int, student_id: int = None):
    query =db.query(Lesson).filter(Lesson.teacher_id == teacher_id, Lesson.paid_amount != Lesson.price)
    if student_id is not None:
        query = query.filter(Lesson.student_id == student_id)
    return query.all()

def create_lesson_for_student(db: Session, student_id: int, teacher_id: int, lesson_in: LessonCreate):
    db_lesson = Lesson(**lesson_in.dict(), student_id=student_id, teacher_id=teacher_id)
    db.add(db_lesson)
    db.commit()
    db.refresh(db_lesson)
    return db_lesson