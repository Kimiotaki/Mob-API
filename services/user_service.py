from repositories.user_repository import UserRepository


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def get_all_users(self):
        users = await self.user_repository.find_all_users()
        return [
            {
                "id": str(user["_id"]),
                "email": user["email"],
                "role": user["role"],
                "created_by": user["created_by"],
                "created_at": user["created_at"],
                "modified_by": user["modified_by"],
                "modified_at": user["modified_at"],
            }
            for user in users
        ]
