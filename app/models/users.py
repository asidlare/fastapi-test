from datetime import date
from re import match
from sqlalchemy.dialects.postgresql import DATE
from sqlalchemy import BIGINT, VARCHAR
from sqlalchemy.orm import Mapped, mapped_column, validates
from typing import Optional

from app.models.utils import TimestampMixin
from app.services.database import Base


class User(Base, TimestampMixin):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(BIGINT, primary_key=True)
    email: Mapped[str] = mapped_column(VARCHAR(255), unique=True, nullable=False)
    first_name: Mapped[Optional[str]] = mapped_column(VARCHAR(255), nullable=True)
    last_name: Mapped[Optional[str]] = mapped_column(VARCHAR(255), nullable=True)
    date_of_birth: Mapped[Optional[date]] = mapped_column(DATE, nullable=True)

    @validates("email")
    def validate_email(self, key: str, address: str) -> str:
        pattern = r'^[\w\.-]+@[a-zA-Z\d-]+\.[a-zA-Z]{2,}$'
        if not match(pattern, address):
            raise ValueError(f"Invalid email address: {address}")
        return address
