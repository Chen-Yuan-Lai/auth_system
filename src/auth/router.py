from fastapi import APIRouter, status

from src.auth.schemas import User

router = APIRouter()


@router.post("/user", status_code=status.HTTP_201_CREATED)
async def createUser(user: User):
    return user
