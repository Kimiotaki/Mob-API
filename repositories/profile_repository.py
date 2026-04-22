from typing import Any

from db.database import db

ProfileDocument = dict[str, Any]


class ProfileRepository:
    def __init__(self):
        self.collection = db["profiles"]

    async def find_by_user_id(self, user_id: str) -> ProfileDocument | None:
        return await self.collection.find_one({"user_id": user_id})

    async def upsert_profile(
        self,
        user_id: str,
        profile_data: dict[str, Any],
    ) -> ProfileDocument | None:
        await self.collection.update_one(
            {"user_id": user_id},
            profile_data,
            upsert=True,
        )
        return await self.find_by_user_id(user_id)
