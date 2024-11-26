from datetime import date, datetime
from pydantic import BaseModel, ConfigDict, EmailStr, field_validator
from typing import Optional


class UserBase(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    date_of_birth: Optional[date] = None

    @field_validator('date_of_birth')
    @classmethod
    def validate_date_of_birth(cls, date_of_birth: date) -> date:
        if date_of_birth and (date.today() - date_of_birth).days / 365.25 < 18:
            raise ValueError("age must be more that 18 years old")
        return date_of_birth


class UserCreate(UserBase):
    email: EmailStr


class UserUpdate(UserBase):
    email: Optional[EmailStr] = None


class UserResponse(UserCreate):
    user_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
