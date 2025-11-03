"""Authentication service orchestrating login and refresh flows."""
from datetime import datetime, timedelta, timezone
import hashlib
from sqlalchemy.orm import Session
from fastapi import HTTPException

from db.repositories import (
    repo_validate_login,
    repo_issue_refresh_token,
    repo_validate_refresh_token_and_get_user,
    repo_rotate_refresh_token_and_issue,
)
from db import models
from core.settings import settings
from utils.security import verify_password, create_access_token, generate_refresh_token

def login_user(db: Session, email: str, password: str):
    user = repo_validate_login(db, email, password, verify_password)
    access = create_access_token(str(user.id), {"is_manager": user.is_manager, "email": user.email})
    raw_refresh = generate_refresh_token()
    expires_at = datetime.now(timezone.utc) + timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
    repo_issue_refresh_token(db, employee_id=user.id, raw_token=raw_refresh, expires_at=expires_at)
    return {
        "access_token": access,
        "refresh_token": raw_refresh,
        "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    }


def refresh_tokens(db: Session, raw_refresh: str):
    user, old_rt = repo_validate_refresh_token_and_get_user(db, raw_refresh)
    new_raw = repo_rotate_refresh_token_and_issue(db, old_rt, user.id)
    access = create_access_token(str(user.id), {"is_manager": user.is_manager, "email": user.email})
    return {
        "access_token": access,
        "refresh_token": new_raw,
        "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    }
