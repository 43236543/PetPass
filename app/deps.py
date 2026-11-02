from collections.abc import Generator
from fastapi import Depends, HTTPException, Request, status
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import User

def get_db() -> Generator[Session, None, None]:
    """Создаёт сессию базы данных для одного запроса."""

    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


def get_current_user(
    request: Request,
    db: Session = Depends(get_db),
) -> User:
    """Получает текущего пользователя из сессии."""

    user_id = request.session.get("user_id")

    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Необходимо войти в аккаунт",
        )

    user = db.get(User, user_id)

    if user is None:
        request.session.clear()

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Пользователь не найден",
        )

    return user