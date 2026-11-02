from datetime import date
from sqlalchemy import (
    Boolean,
    Date,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    middle_name: Mapped[str | None] = mapped_column(String(100), nullable=True)

    username: Mapped[str] = mapped_column(
        String(50), unique=True, nullable=False, index=True
    )
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)

    pets: Mapped[list["Pet"]] = relationship(back_populates="owner")


class Pet(Base):
    __tablename__ = "pets"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    owner_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), nullable=False
    )

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    species: Mapped[str] = mapped_column(String(50), nullable=False)
    breed: Mapped[str | None] = mapped_column(String(100), nullable=True)
    birth_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    weight: Mapped[float | None] = mapped_column(Float, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    owner: Mapped["User"] = relationship(back_populates="pets")
    vet_records: Mapped[list["VetRecord"]] = relationship(
        back_populates="pet"
    )

class RecordType(Base):
    __tablename__ = "record_types"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    name: Mapped[str] = mapped_column(
        String(100), unique=True, nullable=False
    )

    vet_records: Mapped[list["VetRecord"]] = relationship(
        back_populates="record_type"
    )

class VetRecord(Base):
    __tablename__ = "vet_records"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    pet_id: Mapped[int] = mapped_column(
        ForeignKey("pets.id"), nullable=False
    )

    record_type_id: Mapped[int] = mapped_column(
        ForeignKey("record_types.id"), nullable=False
    )

    title: Mapped[str] = mapped_column(String(150), nullable=False)
    record_date: Mapped[date] = mapped_column(Date, nullable=False)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    completed: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )

    pet: Mapped["Pet"] = relationship(back_populates="vet_records")
    record_type: Mapped["RecordType"] = relationship(
        back_populates="vet_records"
    )
