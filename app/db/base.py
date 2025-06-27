# app/db/base.py
from sqlalchemy.orm import DeclarativeBase

# Baza dla wszystkich modeli SQLAlchemy
class Base(DeclarativeBase):
    pass