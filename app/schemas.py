from pydantic import BaseModel, ConfigDict, Field
from datetime import date

class UserRegister(BaseModel):
    last_name: str = Field(min_length=1, max_length=100)
    first_name: str = Field(min_length=1, max_length=100)
    middle_name: str | None = Field(default=None, max_length=100)
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=8, max_length=128)

class UserLogin(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=8, max_length=128)

class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    last_name: str
    first_name: str
    middle_name: str | None
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