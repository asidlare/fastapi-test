from sqlalchemy import (
    BigInteger,
    Column,
    Sequence,
    String,
    select
)
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(
        "id",
        BigInteger,
        Sequence("user_id_seq", start=1),
        primary_key=True
    )
    email = Column(String, unique=True, nullable=False)
    first_name = Column(String(length=255), nullable=True)
    last_name = Column(String(length=255), nullable=True)

    @classmethod
    async def create(cls, db: AsyncSession, **kwargs):
        transaction = cls(**kwargs)
        db.add(transaction)
        await db.commit()
        await db.refresh(transaction)
        return transaction

    @classmethod
    async def get(cls, db: AsyncSession, id: int):
        try:
            transaction = await db.get(cls, id)
        except NoResultFound:
            return None
        return transaction

    @classmethod
    async def get_all(cls, db: AsyncSession):
        return (await db.execute(select(cls))).scalars().all()
