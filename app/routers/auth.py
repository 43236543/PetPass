from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy import select, or_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.deps import get_db, get_current_user
from app.models import User
from app.schemas import UserRegister, UserLogin, UserOut
from app.security import hash_password, verify_password


router = APIRouter(
    prefix="/api/auth",
    tags=["Авторизация"],
)


@router.post(
    "/register",
    response_model=UserOut,
    status_code=status.HTTP_201_CREATED,
)
def register(
    user_data: UserRegister,
    db: Session = Depends(get_db),
):
    """Регистрирует нового пользователя."""

    existing_user = db.scalar(
        select(User).where(
            or_(
                User.username == user_data.username,
                User.phone == user_data.phone,
                User.email == user_data.email,
            )
        )
    )

    if existing_user is not None:
        if existing_user.username == user_data.username:
            detail = "Пользователь с таким логином уже существует"
        elif existing_user.phone == user_data.phone:
            detail = "Пользователь с таким телефоном уже существует"
        else:
            detail = "Пользователь с такой почтой уже существует"

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=detail,
        )

    new_user = User(
        last_name=user_data.last_name,
        first_name=user_data.first_name,
        middle_name=user_data.middle_name,
        phone=user_data.phone,
        email=str(user_data.email),
        username=user_data.username,
        password_hash=hash_password(user_data.password),
    )

    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Логин, телефон или почта уже используются",
        )

    return new_user


@router.post("/login", response_model=UserOut)
def login(
    user_data: UserLogin,
    request: Request,
    db: Session = Depends(get_db),
):
    """Выполняет вход пользователя в систему."""

    user = db.scalar(
        select(User).where(User.username == user_data.username)
    )

    if user is None or not verify_password(
        user_data.password,
        user.password_hash,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный логин или пароль",
        )

    request.session.clear()
    request.session["user_id"] = user.id

    return user


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(request: Request):
    """Завершает сессию пользователя."""

    request.session.clear()

    return None


@router.get("/me", response_model=UserOut)
def get_me(
    current_user: User = Depends(get_current_user),
):
    """Возвращает данные текущего пользователя."""

    return current_user
