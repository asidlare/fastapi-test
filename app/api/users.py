from sqlalchemy import select, update, delete
from sqlalchemy.dialects.postgresql import insert, dialect
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from typing import Optional

from app.models import User


async def create_user(
    db_engine: AsyncEngine,
    data: dict,
) -> User:
    async with db_engine.begin() as conn:
        user = insert(User).values(**data).on_conflict_do_update(
            index_elements=['email'],
            set_={'email': data["email"]}
        ).returning(User)
        result = await conn.execute(user)
        result = result.fetchone()
    return result


async def get_user_by_id(db_session: AsyncSession, user_id: int) -> Optional[User]:
    query = select(User).where(User.user_id == user_id)
    result = await db_session.execute(query)
    result = result.scalars().one_or_none()
    return result


async def get_user_by_email(db_session: AsyncSession, email: str) -> Optional[User]:
    query = select(User).where(User.email == email)
    result = await db_session.execute(query)
    result = result.scalars().one_or_none()
    return result


async def update_user(db_engine: AsyncEngine, user_id: int, data: dict) -> Optional[User]:
    async with db_engine.begin() as conn:
        query = update(User).where(User.user_id == user_id).values(
            **data).returning(User)
        query.compile(dialect=dialect())
        result = await conn.execute(query)
        result = result.one_or_none()
    return result


async def delete_user(db_session: AsyncSession, user_id: int) -> None:
    async with db_session.begin():
        query = delete(User).where(User.user_id == user_id)
        await db_session.execute(query)
