from pydantic import BaseModel, ConfigDict, Field, EmailStr
from datetime import date

class UserRegister(BaseModel):
    last_name: str = Field(min_length=1, max_length=100)
    first_name: str = Field(min_length=1, max_length=100)
    middle_name: str | None = Field(default=None, max_length=100)
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=8, max_length=128)
    phone: str = Field(min_length=5, max_length=20)
    email: EmailStr

class UserLogin(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=8, max_length=128)


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    last_name: str
    first_name: str
    middle_name: str | None
    phone: str | None
    email: EmailStr | None
    username: str


class PetCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    species: str = Field(min_length=1, max_length=50)
    breed: str | None = Field(default=None, max_length=100)
    birth_date: date | None = None
    weight: float | None = Field(default=None, gt=0)
    is_active: bool = True


class PetUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    species: str | None = Field(default=None, min_length=1, max_length=50)
    breed: str | None = Field(default=None, max_length=100)
    birth_date: date | None = None
    weight: float | None = Field(default=None, gt=0)
    is_active: bool | None = None


class PetOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    species: str
    breed: str | None
    birth_date: date | None
    weight: float | None
    is_active: bool

from datetime import date


class RecordCreate(BaseModel):
    record_type_id: int = Field(gt=0)
    title: str = Field(min_length=1, max_length=150)
    record_date: date
    notes: str | None = None
    completed: bool = False


class RecordUpdate(BaseModel):
    record_type_id: int | None = Field(default=None, gt=0)
    title: str | None = Field(default=None, min_length=1, max_length=150)
    record_date: date | None = None
    notes: str | None = None
    completed: bool | None = None


class RecordOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    pet_id: int
    record_type_id: int
    title: str
    record_date: date
    notes: str | None
    completed: bool