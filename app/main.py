# app/main.py
from fastapi import FastAPI
from app.models import teacher, student
from app.api.v1.api import api_router
from app.core.config import settings

app = FastAPI(
    title="Grafik Korepetytora API",
    openapi_url="/api/v1/openapi.json"
)

app.include_router(api_router, prefix="/api/v1")