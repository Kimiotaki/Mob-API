from datetime import datetime, timedelta, timezone
from hashlib import sha256
from typing import Any
from uuid import uuid4
from jose import JWTError, jwt
from passlib.context import CryptContext
from core.config import settings

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

def hash_password(password: str) -> str:
    """Hash a password."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password."""
    return pwd_context.verify(plain_password, hashed_password)

def _create_token(data: dict, token_type: str, expires_delta: timedelta) -> str:
    to_encode = data.copy()
    now = datetime.now(timezone.utc)
    expire = now + expires_delta
    to_encode.update({
        "exp": expire,
        "iat": now,
        "type": token_type,
        "jti": str(uuid4()),
    })
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGO)
    return encoded_jwt

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """Create an access token."""
    token_expiry = expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return _create_token(data, "access", token_expiry)

def create_refresh_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """Create a refresh token."""
    token_expiry = expires_delta or timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    return _create_token(data, "refresh", token_expiry)

def verify_token(token: str, expected_type: str) -> dict[str, Any] | None:
    """Verify a token and match its type."""
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGO])
        if payload.get("type") != expected_type:
            return None
        return payload
    except JWTError:
        return None

def verify_access_token(token: str) -> dict[str, Any] | None:
    """Verify an access token."""
    return verify_token(token, "access")

def verify_refresh_token(token: str) -> dict[str, Any] | None:
    """Verify a refresh token."""
    return verify_token(token, "refresh")

def hash_token(token: str) -> str:
    """Hash a token before storing it."""
    return sha256(token.encode("utf-8")).hexdigest()
