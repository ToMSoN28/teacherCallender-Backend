from pydantic import BaseModel, EmailStr

class TeacherBase(BaseModel):
    email: EmailStr

class TeacherCreate(TeacherBase):
    password: str

class Teacher(TeacherBase):
    id: int

    class Config:
        from_attributes = True