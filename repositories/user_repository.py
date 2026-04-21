from db.database import db

class UserRepository:
    def __init__(self):
        self.collection = db["users"]

    async def create_user(self, user_data):
        result = await self.collection.insert_one(user_data)
        return str(result.inserted_id)

    async def find_user_by_email(self, email):
        user = await self.collection.find_one({"email": email})
        return user

    async def find_all_users(self):
        cursor = self.collection.find({}, {"password": 0}).sort("created_at", -1)
        return await cursor.to_list(length=None)
