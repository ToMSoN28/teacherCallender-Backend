from sqlalchemy.orm import Session, joinedload
from app.models.lesson import Lesson
from app.schemas.lesson import LessonCreate
from app.schemas.lesson_serie import LessonSerieCreate
from app.models.lesson_serie import LessonSerie
from datetime import date, datetime, timedelta

def get_lesson_by_id(db: Session, lesson_id: int, teacher_id: int = None, extended: bool = False):
    query = db.query(Lesson).filter(Lesson.id == lesson_id)
    if teacher_id:
        query = query.filter(Lesson.teacher_id == teacher_id)
    if extended:
        query = query.options(joinedload(Lesson.student))
    return query.first()

def check_empty_space_for_lesson(db: Session, teacher_id: int, date: date, start_time: str, end_time: str, serie_id: int = None):
    query = db.query(Lesson).filter(
        Lesson.teacher_id == teacher_id,
        Lesson.date == date,
        Lesson.start_time < end_time,
        Lesson.end_time > start_time
    )
    if serie_id:
        query = query.filter(Lesson.lesson_serie_id != serie_id)
    return query.first() is None

def create_lesson_for_student(db: Session, student_id: int, teacher_id: int, lesson_in: LessonCreate):
    empty_space = check_empty_space_for_lesson(db, teacher_id, lesson_in.date, lesson_in.start_time, lesson_in.end_time)
    if empty_space:
        db_lesson = Lesson(**lesson_in.dict(), student_id=student_id, teacher_id=teacher_id)
        if db_lesson.start_time >= db_lesson.end_time:
            raise ValueError("Start time must be before end time.")
        if db_lesson.price < 0:
            raise ValueError("Price cannot be negative.")
        db.add(db_lesson)
        db.commit()
        db.refresh(db_lesson)
        return db_lesson
    else:
        raise ValueError("The time slot is already booked for this teacher on this date.")

def get_lessons_by_student(db: Session, student_id: int, teacher_id: int = None, start_date: date = None, end_date: date = None):
    query = db.query(Lesson).filter(Lesson.student_id == student_id and teacher_id == teacher_id)
    if start_date:
        query = query.filter(Lesson.date >= start_date)
    if end_date:
        query = query.filter(Lesson.date <= end_date)
    return query.all()

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
    data = lesson_in.dict(exclude_unset=True)

    new_date = data.get("date", lesson.date)
    new_start_time = data.get("start_time", lesson.start_time)
    new_end_time = data.get("end_time", lesson.end_time)

    if "date" in data and "start_time" not in data and "end_time" not in data:
        new_start_time = lesson.start_time.replace(
            year=new_date.year, month=new_date.month, day=new_date.day
        )
        new_end_time = lesson.end_time.replace(
            year=new_date.year, month=new_date.month, day=new_date.day
        )

    if ("start_time" in data or "end_time" in data) and "date" not in data:
        new_start_time = new_start_time.replace(
            year=lesson.date.year, month=lesson.date.month, day=lesson.date.day
        )
        new_end_time = new_end_time.replace(
            year=lesson.date.year, month=lesson.date.month, day=lesson.date.day
        )

    if new_start_time >= new_end_time:
        raise ValueError("Start time must be before end time.")

    empty_space = check_empty_space_for_lesson(
        db, lesson.teacher_id, new_date, new_start_time, new_end_time
    )
    if not empty_space:
        raise ValueError("The time slot is already booked for this teacher on this date.")

    for field, value in data.items():
        setattr(lesson, field, value)

    if "date" in data or "start_time" in data or "end_time" in data:
        lesson.start_time = new_start_time
        lesson.end_time = new_end_time

    db.commit()
    db.refresh(lesson)
    return lesson

def create_lesson_serie(db: Session, serie_in: LessonSerieCreate, teacher_id: int):
    current_date = serie_in.start_date
    weekday = serie_in.weekday
    terminy = []

    while current_date.weekday() != weekday:
        current_date += timedelta(days=1)
    while current_date <= serie_in.end_date:
        start_dt = datetime.combine(current_date, datetime.strptime(serie_in.start_time, "%H:%M").time())
        end_dt = datetime.combine(current_date, datetime.strptime(serie_in.end_time, "%H:%M").time())
        if start_dt >= end_dt:
            raise ValueError("Start time must be before end time.")
        terminy.append((current_date, start_dt, end_dt))
        current_date += timedelta(days=7)

    # EMPTY_SPACE Validation
    for date_, start_dt, end_dt in terminy:
        empty_space = check_empty_space_for_lesson(
            db, serie_in.teacher_id, date_, start_dt, end_dt
        )
        if not empty_space:
            raise ValueError(f"The time slot is already booked for this teacher on {date_}.")

    db_serie = LessonSerie(**serie_in.dict())
    db_serie.teacher_id = teacher_id
    db.add(db_serie)
    db.commit()
    db.refresh(db_serie)

    for date_, start_dt, end_dt in terminy:
        lesson = Lesson(
            topic=serie_in.name or "Lekcja cykliczna",
            date=date_,
            start_time=start_dt,
            end_time=end_dt,
            notes=serie_in.notes,
            price=serie_in.price or 0.00,
            paid_amount=0.00,
            student_id=serie_in.student_id,
            teacher_id=teacher_id,
            lesson_serie_id=db_serie.id
        )
        db.add(lesson)
    db.commit()
    return db_serie

def get_lessons_for_serie(db: Session, serie_id: int, teacher_id: int):
    return db.query(Lesson).filter(
        Lesson.lesson_serie_id == serie_id,
        Lesson.teacher_id == teacher_id
    ).all()