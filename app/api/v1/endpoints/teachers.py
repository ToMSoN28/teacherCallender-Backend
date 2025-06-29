from fastapi import APIRouter, Depends, HTTPException, Query, Body
from datetime import date, datetime,timedelta
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.schemas.teacher import Teacher, TeacherCreate
from app.schemas.lesson import LessonForTeacherCallender, Lesson
from app.crud import crud_teacher, crud_lesson
from app.api import deps
from app.core import security

router = APIRouter()
# --- Auth section ---
@router.post("/register", response_model=Teacher)
def register_teacher(
    teacher_in: TeacherCreate,
    db: Session = Depends(deps.get_db)
):
    try:
        teacher = crud_teacher.register_teacher(db, teacher_in)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return teacher

@router.post("/login")
def login_teacher(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(deps.get_db)
):
    teacher = crud_teacher.authenticate_teacher(
        db, email=form_data.username, password=form_data.password
    )
    if not teacher:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    access_token = security.create_access_token(data={"sub": str(teacher.id)}, expires_delta=timedelta(minutes=60))
    refrash_token = security.create_access_token(data={"sub": str(teacher.id)}, expires_delta=timedelta(days=14))
    return {"access_token": access_token, "token_type": "bearer", "token_expires_in": 3600, "refresh_token": refrash_token}

@router.post("/refresh")
def refresh_access_token(
    refresh_token: str = Body(...),
    db: Session = Depends(deps.get_db)
):
    payload = security.verify_token(refresh_token)
    teacher_id = payload.get("sub")
    if not teacher_id:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    teacher = crud_teacher.get_teacher_by_id(db, teacher_id=int(teacher_id))
    if not teacher:
        raise HTTPException(status_code=401, detail="User not found")
    access_token = security.create_access_token(data={"sub": str(teacher.id)}, expires_delta=timedelta(minutes=60))
    # refrash_token = create_access_token(data={"sub": str(teacher.id)}, expires_delta=timedelta(days=7))
    return {"access_token": access_token, "token_type": "bearer", "token_expires_in": 3600}
