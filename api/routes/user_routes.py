import logging

from fastapi import APIRouter, Depends

from api.deps import get_current_user_context, get_profile_service, get_user_service
from schemas.profile_schema import ProfileResponse, ProfileUpsertRequest
from schemas.user_schema import UserResponse
from services.profile_service import ProfileService
from services.user_service import UserService

router = APIRouter(prefix="/users", tags=["users"])


@router.get("", response_model=list[UserResponse])
async def get_all_users(user_service: UserService = Depends(get_user_service)):
    logging.info("Getting all users")
    return await user_service.get_all_users()


@router.get("/profile", response_model=ProfileResponse)
async def get_my_profile(
    current_user: dict = Depends(get_current_user_context),
    profile_service: ProfileService = Depends(get_profile_service),
):
    logging.info("Getting profile for user_id=%s", current_user["user_id"])
    return await profile_service.get_profile(current_user["user_id"])


@router.patch("/profile", response_model=ProfileResponse)
async def upsert_my_profile(
    request: ProfileUpsertRequest,
    current_user: dict = Depends(get_current_user_context),
    profile_service: ProfileService = Depends(get_profile_service),
):
    logging.info("Upserting profile for user_id=%s", current_user["user_id"])
    return await profile_service.upsert_profile(current_user["user_id"], request)
