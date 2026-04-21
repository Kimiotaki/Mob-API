from datetime import datetime

from pydantic import BaseModel, EmailStr


class UserResponse(BaseModel):
    id: str
    email: EmailStr
    role: int
    created_by: str
    created_at: datetime
    modified_by: str
    modified_at: datetime
