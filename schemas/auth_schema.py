from pydantic import BaseModel, EmailStr, field_validator
from models.user_model import UserRole


class SignupRequest(BaseModel):
    email: EmailStr
    password: str
    role: int

    @field_validator("role")
    @classmethod
    def validate_role(cls, value: int) -> int:
        if not UserRole.has_value(value):
            raise ValueError("Invalid role value")
        return value

class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class RefreshTokenRequest(BaseModel):
    refresh_token: str
