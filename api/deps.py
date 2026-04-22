from fastapi import Depends, HTTPException, Request, status

from core.security import verify_access_token
from repositories.profile_repository import ProfileRepository
from repositories.user_repository import UserRepository
from services.auth_service import AuthService   
from services.profile_service import ProfileService
from services.user_service import UserService


def get_user_repository():
    return UserRepository()


def get_profile_repository():
    return ProfileRepository()


def get_auth_service(repository: UserRepository = Depends(get_user_repository)):
    return AuthService()


def get_user_service(repository: UserRepository = Depends(get_user_repository)):
    return UserService(repository)


def get_profile_service(
    profile_repository: ProfileRepository = Depends(get_profile_repository),
    user_repository: UserRepository = Depends(get_user_repository),
):
    return ProfileService(profile_repository, user_repository)


def get_current_user_context(request: Request):
    payload = getattr(request.state, "auth_payload", None)
    if payload:
        return payload

    auth_header = request.headers.get("Authorization")
    if not auth_header:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header missing",
        )

    token = auth_header.replace("Bearer ", "")
    payload = verify_access_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )

    return payload
