from sqlalchemy.orm import Session, joinedload
from app.models.lesson import Lesson
from app.schemas.lesson import LessonCreate
from datetime import date

def get_lesson_by_id(db: Session, lesson_id: int, teacher_id: int = None, extended: bool = False):
    query = query(Lesson).filter(Lesson.id == lesson_id)
    if teacher_id:
        query = query.filter(Lesson.teacher_id == teacher_id)
    if extended:
        query = query.options(joinedload(Lesson.student))
    return query.first()

def check_empty_space_for_lesson(db: Session, teacher_id: int, date: date, start_time: str, end_time: str):
    query = db.query(Lesson).filter(
        Lesson.teacher_id == teacher_id,
        Lesson.date == date,
        Lesson.start_time < end_time,
        Lesson.end_time > start_time
    )
    return query.first() is None

def create_lesson_for_student(db: Session, student_id: int, teacher_id: int, lesson_in: LessonCreate):
    empty_space = check_empty_space_for_lesson(db, teacher_id, lesson_in.date, lesson_in.start_time, lesson_in.end_time)
    if empty_space:
        db_lesson = Lesson(**lesson_in.dict(), student_id=student_id, teacher_id=teacher_id)
        db.add(db_lesson)
        db.commit()
        db.refresh(db_lesson)
        return db_lesson
    else:
        raise ValueError("The time slot is already booked for this teacher on this date.")

def get_lessons_by_student(db: Session, student_id: int, teacher_id: int = None):
    return db.query(Lesson).filter(Lesson.student_id == student_id and teacher_id == teacher_id).all()

def get_lessons_for_teacher(db: Session, teacher_id: int, student_id: int = None, start_date: date = None, end_date: date = None, unpaid: bool = False):
    query = db.query(Lesson).options(joinedload(Lesson.student)).filter(Lesson.teacher_id == teacher_id)
    if start_date:
        query = query.filter(Lesson.date >= start_date)
    if end_date:
        query = query.filter(Lesson.date <= end_date)
    if student_id:
        query = query.filter(Lesson.student_id == student_id)
    if unpaid:
        query = query.filter(Lesson.paid_amount != Lesson.price)
    return query.all()

def update_lesson(db: Session, lesson: Lesson, lesson_in):
    for field, value in lesson_in.dict(exclude_unset=True).items():
        setattr(lesson, field, value)
    db.commit()
    db.refresh(lesson)
    return lesson