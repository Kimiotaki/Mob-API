from fastapi import Depends
from repositories.user_repository import UserRepository
from services.auth_service import AuthService   
from services.user_service import UserService

def get_user_repository():
    return UserRepository()

def get_auth_service(repository: UserRepository = Depends(get_user_repository)):
    return AuthService()

def get_user_service(repository: UserRepository = Depends(get_user_repository)):
    return UserService(repository)
