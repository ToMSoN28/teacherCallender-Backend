# app/crud/crud_student.py
from sqlalchemy.orm import Session
from app.models.student import Student
from app.schemas.student import StudentCreate, StudentUpdate

def get_student(db: Session, teacher_id: int, student_id: int):
    return db.query(Student).filter(Student.id == student_id and Student.teacher_id == teacher_id).first()

def get_students(db: Session, teacher_id: int, skip: int = 0, limit: int = 100):
    return db.query(Student).filter(Student.teacher_id ==teacher_id).offset(skip).limit(limit).all()

def create_student(db: Session, teacher_id: int, student: StudentCreate):
    db_student = Student(
        first_name=student.first_name,
        last_name=student.last_name,
        email=student.email,
        teacher_id=teacher_id
    )
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student