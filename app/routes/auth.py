from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import timedelta
from app.core.security import create_jwt_token, verify_password, get_password_hash
from app.models.user import User
from app.schemas.auth import Token, WebAuthnRegistrationStart, WebAuthnRegistrationFinish
from app.core.config import settings
from .deps import get_db

router = APIRouter()

@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    user = await db.execute(User).where(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": create_jwt_token(
            data={"sub": user.email}, 
            expires_delta=access_token_expires
        ),
        "token_type": "bearer"
    }
