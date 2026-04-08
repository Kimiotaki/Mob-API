from pydantic import BaseModel, EmailStr
from models.user_model import UserRole

class SignupRequest(BaseModel):
    email: EmailStr
    password: str
    role: UserRole

class LoginRequest(BaseModel):
    email: EmailStr
    password: str