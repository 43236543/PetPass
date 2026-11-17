from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.deps import get_db, get_current_user
from app.models import Pet, VetRecord, RecordType, User
from app.schemas import RecordCreate, RecordUpdate, RecordOut

router = APIRouter(
    prefix="/api",
    tags=["Ветеринарные записи"],
)

@router.get(
    "/pets/{pet_id}/records",
    response_model=list[RecordOut],
)
def get_pet_records(
    pet_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    pet = db.scalar(
        select(Pet).where(
            Pet.id == pet_id,
            Pet.owner_id == current_user.id,
        )
    )

    if pet is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Питомец не найден",
        )

    statement = select(VetRecord).where(
        VetRecord.pet_id == pet_id
    )

    records = db.scalars(statement).all()
    return records


@router.post(
    "/pets/{pet_id}/records",
    response_model=RecordOut,
    status_code=status.HTTP_201_CREATED,
)
def create_pet_record(
    pet_id: int,
    record_data: RecordCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    pet = db.scalar(
        select(Pet).where(
            Pet.id == pet_id,
            Pet.owner_id == current_user.id,
        )
    )

    if pet is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Питомец не найден",
        )

    record_type = db.get(
        __import__("app.models", fromlist=["RecordType"]).RecordType,
        record_data.record_type_id,
    )

    if record_type is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Тип ветеринарной записи не найден",
        )

    new_record = VetRecord(
        pet_id=pet.id,
        record_type_id=record_data.record_type_id,
        title=record_data.title,
        record_date=record_data.record_date,
        notes=record_data.notes,
        completed=record_data.completed,
    )

    db.add(new_record)
    db.commit()
    db.refresh(new_record)

    return new_record

@router.patch(
    "/records/{record_id}",
    response_model=RecordOut,
)
def update_record(
    record_id: int,
    record_data: RecordUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    statement = (
        select(VetRecord)
        .join(Pet)
        .where(
            VetRecord.id == record_id,
            Pet.owner_id == current_user.id,
        )
    )

    record = db.scalar(statement)

    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ветеринарная запись не найдена",
        )

    update_data = record_data.model_dump(exclude_unset=True)

    if "record_type_id" in update_data:
        record_type = db.get(RecordType, update_data["record_type_id"])

        if record_type is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Тип ветеринарной записи не найден",
            )

    for field, value in update_data.items():
        setattr(record, field, value)

    db.commit()
    db.refresh(record)

    return record

@router.delete(
    "/records/{record_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_record(
    record_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    statement = (
        select(VetRecord)
        .join(Pet)
        .where(
            VetRecord.id == record_id,
            Pet.owner_id == current_user.id,
        )
    )

    record = db.scalar(statement)

    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ветеринарная запись не найдена",
        )

    db.delete(record)
    db.commit()

    return None