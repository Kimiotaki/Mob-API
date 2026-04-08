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