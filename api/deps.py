from fastapi import Depends
from repositories.user_repository import UserRepository
from services.auth_service import AuthService   

def get_user_repository():
    return UserRepository()

def get_auth_service(repository: UserRepository = Depends(get_user_repository)):
    return AuthService()