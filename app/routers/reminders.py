
from datetime import date

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.deps import get_db, get_current_user
from app.models import Pet, VetRecord, RecordType, User


router = APIRouter(
    prefix="/api/reminders",
    tags=["Напоминания"],
)


@router.get("/next")
def get_next_reminders(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Возвращает предстоящие незавершённые процедуры."""

    statement = (
        select(
            VetRecord.id,
            VetRecord.title,
            VetRecord.record_date,
            VetRecord.notes,
            Pet.name.label("pet_name"),
            RecordType.name.label("record_type"),
        )
        .join(Pet, VetRecord.pet_id == Pet.id)
        .join(RecordType, VetRecord.record_type_id == RecordType.id)
        .where(
            Pet.owner_id == current_user.id,
            VetRecord.completed.is_(False),
            VetRecord.record_date >= date.today(),
        )
        .order_by(VetRecord.record_date.asc())
        .limit(10)
    )

    reminders = db.execute(statement).all()

    return [
        {
            "id": reminder.id,
            "title": reminder.title,
            "record_date": reminder.record_date,
            "notes": reminder.notes,
            "pet_name": reminder.pet_name,
            "record_type": reminder.record_type,
        }
        for reminder in reminders
    ]
