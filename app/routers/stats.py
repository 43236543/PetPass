from fastapi import APIRouter, Depends
from sqlalchemy import select, func
from sqlalchemy.orm import Session

from app.deps import get_db, get_current_user
from app.models import Pet, VetRecord, User


router = APIRouter(
    prefix="/api",
    tags=["Статистика"],
)


@router.get("/stats")
def get_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Возвращает статистику питомцев текущего пользователя."""

    # Общее количество питомцев
    total_pets = db.scalar(
        select(func.count(Pet.id)).where(
            Pet.owner_id == current_user.id
        )
    )

    # Количество питомцев по видам
    species_result = db.execute(
        select(
            Pet.species,
            func.count(Pet.id),
        )
        .where(Pet.owner_id == current_user.id)
        .group_by(Pet.species)
        .order_by(Pet.species)
    ).all()

    pets_by_species = [
        {
            "species": species,
            "count": count,
        }
        for species, count in species_result
    ]

    # Средний вес питомцев
    average_weight = db.scalar(
        select(func.avg(Pet.weight)).where(
            Pet.owner_id == current_user.id,
            Pet.weight.is_not(None),
        )
    )

    # Общее количество ветеринарных записей
    total_records = db.scalar(
        select(func.count(VetRecord.id))
        .join(Pet, VetRecord.pet_id == Pet.id)
        .where(Pet.owner_id == current_user.id)
    )

    return {
        "total_pets": total_pets or 0,
        "pets_by_species": pets_by_species,
        "average_weight": (
            round(average_weight, 2)
            if average_weight is not None
            else None
        ),
        "total_records": total_records or 0,
    }
