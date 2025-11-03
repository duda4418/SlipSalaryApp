from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
import jwt
from db import session, models
from core.settings import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

CREDENTIALS_EXCEPTION = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})

def get_current_employee(token: str = Depends(oauth2_scheme), db: Session = Depends(session.get_db)) -> models.Employee:
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        sub = payload.get("sub")
        if sub is None:
            raise CREDENTIALS_EXCEPTION
    except jwt.PyJWTError:
        raise CREDENTIALS_EXCEPTION
    user = db.get(models.Employee, sub)
    if not user or not user.is_active:
        raise CREDENTIALS_EXCEPTION
    return user

def require_manager(current: models.Employee = Depends(get_current_employee)) -> models.Employee:
    if not current.is_manager:
        raise HTTPException(status_code=403, detail="Manager access required")
    return current
