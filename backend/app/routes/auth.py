from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.auth import UserCreate, UserResponse, Token, LoginRequest, ApiResponse
from app.services import auth_service

router = APIRouter()

@router.post("/register", response_model=ApiResponse[UserResponse])
async def register(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    user = await auth_service.register_user(db, user_in)
    return {"data": user}

@router.post("/login", response_model=Token)
async def login(login_req: LoginRequest, db: AsyncSession = Depends(get_db)):
    # Adapt to service expecting form-like object with username/password
    # Since we use JSON interface as per contract
    class LoginData:
        username = login_req.username
        password = login_req.password
        
    return await auth_service.login_access_token(db, LoginData())
