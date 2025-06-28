from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.models.teacher import Teacher
from app.schemas.teacher import TeacherCreate
from passlib.context import CryptContext
from app.db.session import SessionLocal

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
def get_teacher_by_email(db: Session, email: str):
    return db.query(Teacher).filter(Teacher.email == email).first()

def get_teacher_by_id(db: Session, teacher_id: int):
    return db.query(Teacher).filter(Teacher.id == teacher_id).first()

def create_teacher(db: Session, teacher: TeacherCreate):
    hashed_password = pwd_context.hash(teacher.password)
    db_teacher = Teacher(email=teacher.email, hashed_password=hashed_password)
    db.add(db_teacher)
    db.commit()
    db.refresh(db_teacher)
    return db_teacher

def register_teacher(db: Session, teacher: TeacherCreate):
    if get_teacher_by_email(db, teacher.email):
        raise ValueError("Email already registered")
    return create_teacher(db, teacher)

def authenticate_teacher(db: Session, email: str, password: str):
    teacher = get_teacher_by_email(db, email)
    if not teacher or not pwd_context.verify(password, teacher.hashed_password):
        return None
    return teacher