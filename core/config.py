from pydantic.v1 import BaseSettings

class Settings(BaseSettings):
    """Application settings."""
    app_name: str = "My FastAPI Application"
    debug: bool = True
    MONGO_URL: str = "mongodb://localhost:27017"
    DB_NAME: str = "mob_dev"
    JWT_SECRET: str = "supersecret"
    JWT_ALGO: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

settings = Settings()