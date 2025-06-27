from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.schemas.teacher import Teacher, TeacherCreate
from app.crud import crud_teacher
from app.api import deps
from app.core.security import create_access_token

router = APIRouter()

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
    access_token = create_access_token(data={"sub": str(teacher.id)})
    return {"access_token": access_token, "token_type": "bearer"}