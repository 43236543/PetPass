from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.deps import get_db, get_current_user
from app.models import RecordType, User


router = APIRouter(
    prefix="/api/record-types",
    tags=["Типы ветеринарных записей"],
)


@router.get("/")
def get_record_types(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Возвращает список доступных типов ветеринарных записей."""

    statement = select(RecordType).order_by(RecordType.id.asc())

    record_types = db.scalars(statement).all()

    return [
        {
            "id": record_type.id,
            "name": record_type.name,
        }
        for record_type in record_types
    ]
