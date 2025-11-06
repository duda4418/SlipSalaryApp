from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import datetime, timedelta, timezone
import hashlib, uuid
from core.settings import settings
from db import models

__all__ = [
    'repo_create_refresh_token',
    'repo_get_refresh_token_by_hash',
    'repo_rotate_refresh_token',
    'repo_issue_refresh_token',
    'repo_validate_refresh_token_and_get_user',
    'repo_rotate_refresh_token_and_issue',
]

def repo_create_refresh_token(db: Session, **data):
    token = models.RefreshToken(**data)
    db.add(token)
    db.commit()
    db.refresh(token)
    return token

def repo_get_refresh_token_by_hash(db: Session, token_hash: str):
    return db.query(models.RefreshToken).filter(models.RefreshToken.token_hash == token_hash).first()

def repo_rotate_refresh_token(db: Session, old_token: models.RefreshToken, new_token: models.RefreshToken):
    old_token.revoked = True
    old_token.replaced_by = new_token.id
    db.add(new_token)
    db.commit()
    db.refresh(new_token)
    return new_token

def repo_issue_refresh_token(db: Session, employee_id, raw_token: str, expires_at):
    token_hash = hashlib.sha256(raw_token.encode()).hexdigest()
    return repo_create_refresh_token(db, employee_id=employee_id, token_hash=token_hash, expires_at=expires_at)

def repo_validate_refresh_token_and_get_user(db: Session, raw_token: str):
    token_hash = hashlib.sha256(raw_token.encode()).hexdigest()
    rt = repo_get_refresh_token_by_hash(db, token_hash)
    if not rt or rt.revoked:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    expires_at = rt.expires_at
    if expires_at.tzinfo is None:
        expires_at = expires_at.replace(tzinfo=timezone.utc)
    if expires_at < datetime.now(timezone.utc):
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    user = db.get(models.Employee, rt.employee_id)
    if not user or not user.is_active:
        raise HTTPException(status_code=401, detail="Inactive user")
    return user, rt

def repo_rotate_refresh_token_and_issue(db: Session, old_rt: models.RefreshToken, employee_id) -> str:
    new_raw = f"{uuid.uuid4()}:{datetime.now(timezone.utc).timestamp()}"
    new_hash = hashlib.sha256(new_raw.encode()).hexdigest()
    new_rt = models.RefreshToken(
        employee_id=employee_id,
        token_hash=new_hash,
        expires_at=datetime.now(timezone.utc) + timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES),
    )
    old_rt.revoked = True
    old_rt.replaced_by = new_rt.id
    db.add(new_rt)
    db.commit()
    db.refresh(new_rt)
    return new_raw
