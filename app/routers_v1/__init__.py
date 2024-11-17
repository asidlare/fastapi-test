from fastapi import APIRouter


router_v1 = APIRouter()


@router_v1.get("/")
async def root():
    return {"message": "Hello test FastAPI!"}
