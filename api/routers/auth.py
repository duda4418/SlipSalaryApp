from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db import session
from services.auth_service import login_user, refresh_tokens
from api.schemas_auth import LoginRequest, RefreshRequest, TokenResponse

auth_router = APIRouter(prefix="/auth", tags=["auth"])

@auth_router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, db: Session = Depends(session.get_db)):
    result = login_user(db, data.email, data.password)
    return TokenResponse(
        access_token=result["access_token"],
        expires_in=result["expires_in"],
        refresh_token=result["refresh_token"],
    )

@auth_router.post("/refresh", response_model=TokenResponse)
def refresh(data: RefreshRequest, db: Session = Depends(session.get_db)):
    result = refresh_tokens(db, data.refresh_token)
    return TokenResponse(
        access_token=result["access_token"],
        expires_in=result["expires_in"],
        refresh_token=result["refresh_token"],
    )
