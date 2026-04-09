import datetime
from typing import Any

from fastapi import HTTPException, status

from core.config import settings
from repositories.user_repository import UserRepository
from repositories.refresh_token_repository import RefreshTokenRepository
from models.user_model import UserRole

from core.security import (
    create_access_token,
    create_refresh_token,
    hash_password,
    hash_token,
    verify_password,
    verify_refresh_token,
)


class AuthService:
    def __init__(self):
        self.user_repository = UserRepository()
        self.refresh_token_repository = RefreshTokenRepository()

    async def signup(self, email: str, password: str, role: int):
        existing_user = await self.user_repository.find_user_by_email(email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered",
            )

        if not UserRole.has_value(role):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid role value",
            )

        hashed_password = hash_password(password)
        user_data = {
            "email": email,
            "password": hashed_password,
            "role": int(role),
            "created_by": email,
            "created_at": datetime.datetime.now(datetime.timezone.utc),
            "modified_by": email,
            "modified_at": datetime.datetime.now(datetime.timezone.utc),
            "normalized_email": email.upper(),
            
        }
        user_id = await self.user_repository.create_user(user_data)
        return user_id

    async def login(self, email: str, password: str):
        user = await self.user_repository.find_user_by_email(email)
        if not user or not verify_password(password, user["password"]):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )

        return await self._issue_tokens(user)

    async def refresh_access_token(self, refresh_token: str):
        payload = verify_refresh_token(refresh_token)
        if not payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token",
            )

        stored_token = await self.refresh_token_repository.find_active_token(hash_token(refresh_token))
        if not stored_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token expired or revoked",
            )

        user = await self.user_repository.find_user_by_email(stored_token["email"])
        if not user or str(user["_id"]) != payload.get("user_id"):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token is no longer valid",
            )

        old_token_hash = hash_token(refresh_token)
        token_response = await self._issue_tokens(user)
        await self.refresh_token_repository.revoke_token(
            old_token_hash,
            replaced_by_hash=hash_token(token_response["refresh_token"]),
        )
        return token_response

    async def logout(self, refresh_token: str):
        payload = verify_refresh_token(refresh_token)
        if not payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token",
            )

        await self.refresh_token_repository.revoke_token(hash_token(refresh_token))
        return {"message": "Logged out successfully"}

    async def _issue_tokens(self, user: dict[str, Any]):
        user_id = str(user["_id"])
        token_payload = {"user_id": user_id, "role": user["role"]}
        access_token = create_access_token(token_payload)
        refresh_token = create_refresh_token(token_payload)

        refresh_payload = verify_refresh_token(refresh_token)
        if refresh_payload is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to issue refresh token",
            )

        refresh_expires_at = datetime.datetime.fromtimestamp(
            refresh_payload["exp"],
            tz=datetime.timezone.utc,
        )
        refresh_token_hash = hash_token(refresh_token)

        await self.refresh_token_repository.create_refresh_token(
            {
                "user_id": user_id,
                "email": user["email"],
                "token_hash": refresh_token_hash,
                "jti": refresh_payload["jti"],
                "expires_at": refresh_expires_at,
                "revoked_at": None,
                "replaced_by_token_hash": None,
                "created_at": datetime.datetime.now(datetime.timezone.utc),
            }
        )

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "access_token_expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            "refresh_token_expires_in": settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
        }
