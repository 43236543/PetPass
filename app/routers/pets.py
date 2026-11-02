from fastapi import APIRouter, Depends, HTTPException, status
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
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    statement = select(Pet).where(
        Pet.owner_id == current_user.id
    )
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