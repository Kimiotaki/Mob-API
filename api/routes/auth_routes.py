from fastapi import Depends, APIRouter
from schemas.auth_schema import SignupRequest, LoginRequest
from api.deps import get_auth_service   
from services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/signup")
async def signup(request: SignupRequest, auth_service: AuthService = Depends(get_auth_service)):    
    user_id = await auth_service.signup(request.email, request.password, request.role)
    return {"user_id": user_id}

@router.post("/login")
async def login(request: LoginRequest, auth_service: AuthService = Depends(get_auth_service)):    
    access_token = await auth_service.login(request.email, request.password)
    return {"access_token": access_token}