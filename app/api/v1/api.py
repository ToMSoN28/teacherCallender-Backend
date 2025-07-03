from fastapi import APIRouter
from app.api.v1.endpoints import students, teachers, lessons, lessons_serie # importujesz kolejne

api_router = APIRouter()
api_router.include_router(students.router, prefix="/students", tags=["students"])
api_router.include_router(lessons.router, prefix="/lessons", tags=["lessons"])
api_router.include_router(lessons_serie.router, prefix="/series", tags=["lessons_serie"])
api_router.include_router(teachers.router, tags=["users"])