from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine
from typing import Annotated

from app.api.users import (
    create_user,
    get_user_by_id,
    get_user_by_email,
    update_user,
    delete_user,
)
from app.services.database import get_db_session, get_db_engine
from app.schemas.error import ErrorResponse
from app.schemas.users import UserCreate, UserUpdate, UserResponse


users_router = APIRouter()


@users_router.post(
    "/create",
    status_code=status.HTTP_201_CREATED,
    response_model=UserResponse,
)
async def create(
    payload: UserCreate,
    db_engine: Annotated[AsyncEngine, Depends(get_db_engine)]
):
    user = await create_user(
        db_engine=db_engine,
        data=payload.model_dump(exclude_unset=True, exclude_none=True),
    )
    return user


@users_router.get(
    "/get-by-id/{user_id}",
    status_code=status.HTTP_200_OK,
    response_model=UserResponse,
    responses={
        "404": {"model": ErrorResponse, "description": "User not found"},
        "200": {"model": UserResponse, "description": "User found"}
    },
)
async def get_by_id(
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
    user_id: int
):
    user = await get_user_by_id(db_session, user_id)
    if user:
        return user
    return JSONResponse(
        content={"message": "User not found"},
        status_code=status.HTTP_404_NOT_FOUND
    )


@users_router.get(
    "/get-by-email/{email}",
    status_code=status.HTTP_200_OK,
    response_model=UserResponse,
    responses={
        "404": {"model": ErrorResponse, "description": "User not found"},
        "200": {"model": UserResponse, "description": "User found"}
    },
)
async def get_by_email(
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
    email: str,
):
    user = await get_user_by_email(db_session, email)
    if user:
        return user
    return JSONResponse(
        content={"message": "User not found"},
        status_code=status.HTTP_404_NOT_FOUND
    )


@users_router.patch(
    "/update/{user_id}",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=UserResponse,
    responses={
        "400": {"model": ErrorResponse, "description": "User with email exists"},
        "404": {"model": ErrorResponse, "description": "User not found"},
        "200": {"model": UserResponse, "description": "User found"}
    },
)
async def update(
    db_engine: Annotated[AsyncEngine, Depends(get_db_engine)],
    user_id: int,
    payload: UserUpdate,
):
    try:
        user = await update_user(
            db_engine=db_engine,
            user_id=user_id,
            data=payload.model_dump(exclude_unset=True, exclude_none=True),
        )
        if user:
            return user
        return JSONResponse(
            content={"message": "User not found"},
            status_code=status.HTTP_404_NOT_FOUND
        )
    except IntegrityError:
        return JSONResponse(
            content={"message": f"User with email {payload.email} already exists"},
            status_code=status.HTTP_400_BAD_REQUEST
        )


@users_router.delete(
    "/delete/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete(
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
    user_id: int
):
    await delete_user(db_session, user_id)