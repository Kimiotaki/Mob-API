from repositories.user_repository import UserRepository

from core.security import hash_password, verify_password, create_access_token

class AuthService:
    def __init__(self):
        self.user_repository = UserRepository()

    async def signup(self, email: str, password: str, role):
        existing_user = await self.user_repository.find_user_by_email(email)
        if existing_user:
            raise ValueError("Email already registered")

        hashed_password = hash_password(password)
        user_data = {
            "email": email,
            "password": hashed_password,
            "role": role
        }
        user_id = await self.user_repository.create_user(user_data)
        return user_id

    async def login(self, email: str, password: str):
        user = await self.user_repository.find_user_by_email(email)
        if not user or not verify_password(password, user["password"]):
            raise ValueError("Invalid email or password")

        access_token = create_access_token({"user_id": str(user["_id"]), "role": user["role"]})
        return access_token