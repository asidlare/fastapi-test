from fastapi import APIRouter
from .users import users_router


router_v1 = APIRouter()
router_v1.include_router(users_router, prefix="/users")


@router_v1.get("/")
async def root():
    return {"message": "Hello test FastAPI!"}
