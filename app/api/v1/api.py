from fastapi import APIRouter
from app.api.v1.endpoints import students, teachers # importujesz kolejne

api_router = APIRouter()
api_router.include_router(students.router, prefix="/students", tags=["students"])
api_router.include_router(teachers.router, prefix="/teachers", tags=["teachers"])