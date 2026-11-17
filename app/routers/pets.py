from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.deps import get_db, get_current_user
from app.models import Pet, User
from app.schemas import PetCreate, PetUpdate, PetOut

router = APIRouter(
    prefix="/api/pets",
    tags=["Питомцы"],
)

@router.get("/", response_model=list[PetOut])
def get_pets(
    search: str | None = Query(default=None, min_length=1),
    species: str | None = Query(default=None, min_length=1),
    sort_by: str = Query(default="id"),
    sort_order: str = Query(default="asc"),
    limit: int = Query(default=10, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    statement = select(Pet).where(
        Pet.owner_id == current_user.id
    )

    if search:
        statement = statement.where(
            Pet.name.ilike(f"%{search}%")
        )
    if species:
        statement = statement.where(
        Pet.species.ilike(species)
    )

    if sort_by not in ["id", "name", "weight"]:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Недопустимое поле сортировки",
        )

    if sort_order not in ["asc", "desc"]:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Недопустимый порядок сортировки",
        )

    sort_column = getattr(Pet, sort_by)

    if sort_order == "desc":
        statement = statement.order_by(sort_column.desc())
    else:
        statement = statement.order_by(sort_column.asc())

    statement = statement.limit(limit).offset(offset)

    pets = db.scalars(statement).all()
    return pets

@router.post(
    "/",
    response_model=PetOut,
    status_code=status.HTTP_201_CREATED,
)
def create_pet(
    pet_data: PetCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    new_pet = Pet(
        owner_id=current_user.id,
        name=pet_data.name,
        species=pet_data.species,
        breed=pet_data.breed,
        birth_date=pet_data.birth_date,
        weight=pet_data.weight,
        is_active=pet_data.is_active,
    )

    db.add(new_pet)
    db.commit()
    db.refresh(new_pet)

    return new_pet

@router.get("/{pet_id}", response_model=PetOut)
def get_pet(
    pet_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    statement = select(Pet).where(
        Pet.id == pet_id,
        Pet.owner_id == current_user.id,
    )

    pet = db.scalar(statement)

    if pet is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Питомец не найден",
        )

    return pet

@router.patch("/{pet_id}", response_model=PetOut)
def update_pet(
    pet_id: int,
    pet_data: PetUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    statement = select(Pet).where(
        Pet.id == pet_id,
        Pet.owner_id == current_user.id,
    )

    pet = db.scalar(statement)

    if pet is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Питомец не найден",
        )

    update_data = pet_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(pet, field, value)

    db.commit()
    db.refresh(pet)

    return pet

@router.delete(
    "/{pet_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_pet(
    pet_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    statement = select(Pet).where(
        Pet.id == pet_id,
        Pet.owner_id == current_user.id,
    )

    pet = db.scalar(statement)

    if pet is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Питомец не найден",
        )

    db.delete(pet)
    db.commit()

    return None