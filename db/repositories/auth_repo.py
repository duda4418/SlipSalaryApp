from sqlalchemy.orm import Session
from fastapi import HTTPException
from db import models

__all__ = [
    'repo_validate_login',
]

def repo_validate_login(db: Session, email: str, password: str, verify_fn) -> models.Employee:
    """Validate login credentials and return employee or raise HTTP 401."""
    user = db.query(models.Employee).filter(models.Employee.email == email).first()
    if not user or not user.password_hash or not verify_fn(password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    if not user.is_active:
        raise HTTPException(status_code=401, detail="Inactive user")
    return user
