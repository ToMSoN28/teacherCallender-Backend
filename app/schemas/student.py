# app/schemas/student.py
from pydantic import BaseModel, EmailStr
from typing import Optional

# Pola wspólne dla tworzenia i odczytu
class StudentBase(BaseModel):
    first_name: str
    last_name: str
    email: Optional[EmailStr] = None

# Schemat do tworzenia nowego studenta (dane wejściowe)
class StudentCreate(StudentBase):
    pass

# Schemat do aktualizacji studenta (wszystkie pola opcjonalne)
class StudentUpdate(StudentBase):
    first_name: Optional[str] = None
    last_name: Optional[str] = None

# Schemat do odczytu danych studenta (dane wyjściowe z API)
class Student(StudentBase):
    id: int

    class Config:
        from_attributes = True