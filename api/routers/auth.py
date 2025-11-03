from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone
from pydantic import BaseModel

from db import session, models
from utils.security import verify_password, hash_password, create_access_token, generate_refresh_token
from core.settings import settings
import uuid, hashlib

auth_router = APIRouter(prefix="/auth", tags=["auth"])

class LoginRequest(BaseModel):
    email: str
    password: str

class TokenResponse(BaseModel):
    accessToken: str
    tokenType: str = "bearer"
    expiresIn: int
    refreshToken: str | None = None

class RefreshRequest(BaseModel):
    refreshToken: str

@auth_router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, db: Session = Depends(session.get_db)):
    user = db.query(models.Employee).filter(models.Employee.email == data.email).first()
    if not user or not user.password_hash or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    # Access token
    access_token = create_access_token(str(user.id), {"is_manager": user.is_manager, "email": user.email})
    # Refresh token (opaque)
    raw_refresh = generate_refresh_token()
    token_hash = hashlib.sha256(raw_refresh.encode()).hexdigest()
    expires_at = datetime.now(timezone.utc) + timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
    rt = models.RefreshToken(
        employee_id=user.id,
        token_hash=token_hash,
        expires_at=expires_at,
    )
    db.add(rt)
    db.commit()
    return TokenResponse(accessToken=access_token, expiresIn=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60, refreshToken=raw_refresh)

@auth_router.post("/refresh", response_model=TokenResponse)
def refresh(data: RefreshRequest, db: Session = Depends(session.get_db)):
    token_hash = hashlib.sha256(data.refreshToken.encode()).hexdigest()
    rt = db.query(models.RefreshToken).filter(models.RefreshToken.token_hash == token_hash).first()
    if not rt or rt.revoked or rt.expires_at < datetime.now(timezone.utc):
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    user = db.get(models.Employee, rt.employee_id)
    if not user or not user.is_active:
        raise HTTPException(status_code=401, detail="Inactive user")
    # Rotate: revoke old, issue new
    rt.revoked = True
    new_raw = generate_refresh_token()
    new_hash = hashlib.sha256(new_raw.encode()).hexdigest()
    new_rt = models.RefreshToken(
        employee_id=user.id,
        token_hash=new_hash,
        expires_at=datetime.now(timezone.utc) + timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
    )
    rt.replaced_by = new_rt.id
    db.add(new_rt)
    db.commit()
    access_token = create_access_token(str(user.id), {"is_manager": user.is_manager, "email": user.email})
    return TokenResponse(accessToken=access_token, expiresIn=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60, refreshToken=new_raw)
