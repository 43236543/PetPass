from pathlib import Path
from dotenv import load_dotenv
from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from app.routers import auth

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

import os

SECRET_KEY = os.getenv("SECRET_KEY")

if not SECRET_KEY:
    raise RuntimeError("Не найден SECRET_KEY в файле .env")

app = FastAPI(
    title="PetPass",
    description="Система учёта домашних питомцев",
    version="1.0.0",
)

app.add_middleware(
    SessionMiddleware,
    secret_key=SECRET_KEY,
    session_cookie="petpass_session",
    same_site="lax",
    https_only=False,
)

app.include_router(auth.router)

@app.get("/")
def read_root():
    return {"message": "Добро пожаловать в PetPass!"}