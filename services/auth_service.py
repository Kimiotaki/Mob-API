import datetime

from fastapi import HTTPException, status

from repositories.user_repository import UserRepository
from models.user_model import UserRole

from core.security import hash_password, verify_password, create_access_token


class AuthService:
    def __init__(self):
        self.user_repository = UserRepository()

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
            "created_at": datetime.datetime.utcnow(),
            "modified_by": email,
            "modified_at": datetime.datetime.utcnow(),
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

        access_token = create_access_token({"user_id": str(user["_id"]), "role": user["role"]})
        return access_token
