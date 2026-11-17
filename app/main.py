import os
from pathlib import Path
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from app.routers import auth, pets, records, stats, reminders, record_types
from fastapi.responses import FileResponse


BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = BASE_DIR / "app" / "static"

load_dotenv(BASE_DIR / ".env")

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

app.mount(
    "/static",
    StaticFiles(directory=STATIC_DIR),
    name="static",
)

app.include_router(auth.router)
app.include_router(pets.router)
app.include_router(records.router)
app.include_router(stats.router)
app.include_router(reminders.router)
app.include_router(record_types.router)

@app.get("/register.html")
def register_page():
    return FileResponse(STATIC_DIR / "register.html")

@app.get("/login.html")
def login_page():
    return FileResponse(STATIC_DIR / "login.html")


@app.get("/")
def read_root():
    return FileResponse(STATIC_DIR / "main.html")


@app.get("/main.html")
def main_page():
    return FileResponse(STATIC_DIR / "main.html")
