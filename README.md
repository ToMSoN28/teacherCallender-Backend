# TeacherCallender

TeacherCallender is a backend API for managing teachers and their students, built with FastAPI and SQLAlchemy. It provides authentication for teachers and CRUD operations for student management.

## Features

- Teacher registration and login with JWT authentication
- Secure password hashing
- CRUD operations for students (create, read, update, delete)
- PostgreSQL database support
- Environment-based configuration

## Project Structure
app/ main.py # FastAPI application entrypoint models/ # SQLAlchemy models schemas/ # Pydantic schemas crud/ # CRUD logic db/ # Database session and base core/ # Configuration and security api/ # API routers and dependencies alembic/ # Database migrations .env # Environment variables pyproject.toml # Project metadata and dependencies

