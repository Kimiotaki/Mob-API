from fastapi import Depends, APIRouter
from schemas.auth_schema import SignupRequest, LoginRequest, RefreshTokenRequest
from api.deps import get_auth_service   
from services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/signup")
async def signup(request: SignupRequest, auth_service: AuthService = Depends(get_auth_service)):    
    user_id = await auth_service.signup(request.email, request.password, request.role)
    return {"user_id": user_id}

@router.post("/login")
async def login(request: LoginRequest, auth_service: AuthService = Depends(get_auth_service)):    
    return await auth_service.login(request.email, request.password)

@router.post("/refresh")
async def refresh(request: RefreshTokenRequest, auth_service: AuthService = Depends(get_auth_service)):
    return await auth_service.refresh_access_token(request.refresh_token)

@router.post("/logout")
async def logout(request: RefreshTokenRequest, auth_service: AuthService = Depends(get_auth_service)):
    return await auth_service.logout(request.refresh_token)
