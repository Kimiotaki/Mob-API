import logging

from fastapi import APIRouter, Depends

from api.deps import get_user_service
from schemas.user_schema import UserResponse
from services.user_service import UserService

router = APIRouter(prefix="/users", tags=["users"])


@router.get("", response_model=list[UserResponse])
async def get_all_users(user_service: UserService = Depends(get_user_service)):
    logging.info("Getting all users")
    return await user_service.get_all_users()
