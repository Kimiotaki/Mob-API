from datetime import datetime, timezone

from db.database import db


class RefreshTokenRepository:
    def __init__(self):
        self.collection = db["refresh_tokens"]

    async def create_refresh_token(self, token_data: dict):
        result = await self.collection.insert_one(token_data)
        return str(result.inserted_id)

    async def find_active_token(self, token_hash: str):
        now = datetime.now(timezone.utc)
        return await self.collection.find_one(
            {
                "token_hash": token_hash,
                "revoked_at": None,
                "expires_at": {"$gt": now},
            }
        )

    async def revoke_token(self, token_hash: str, replaced_by_hash: str | None = None):
        return await self.collection.update_one(
            {
                "token_hash": token_hash,
                "revoked_at": None,
            },
            {
                "$set": {
                    "revoked_at": datetime.now(timezone.utc),
                    "replaced_by_token_hash": replaced_by_hash,
                }
            },
        )
