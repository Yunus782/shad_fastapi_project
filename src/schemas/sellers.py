from typing import Optional

from pydantic import BaseModel, field_validator, EmailStr, Field
from passlib.context import CryptContext
from pydantic_core import PydanticCustomError


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

__all__ = ["IncomingSeller", "ReturnedAllSellers", "ReturnedSeller"]


class BaseSeller(BaseModel):
    first_name: str = Field(..., min_length=2, max_length=50)
    last_name: str = Field(..., min_length=2, max_length=50)
    email: EmailStr
    password: str


class IncomingSeller(BaseSeller):
    @field_validator("first_name", "last_name")
    @staticmethod
    def validate_name_fields(value: str, field: str):
        if not value.isalpha():
            raise PydanticCustomError("Validation error", f"{field} must contain only letters")
        return value

    @field_validator("password")
    @staticmethod
    def validate_password(value: str):
        if len(value) < 8:
            raise PydanticCustomError("Validation error", "Password must be at least 8 characters long")
        return value


class ReturnedSeller(BaseSeller):
    id: Optional[int] = None

    class Config:
        orm_mode = True
        exclude = {'password'}


class ReturnedAllSellers(BaseModel):
    books: list[ReturnedSeller]
