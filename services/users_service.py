from fastapi import HTTPException
from sqlalchemy.orm import Session
from db import models

def get_users(db: Session):
    return db.query(models.User).all()

def get_user_by_id(db: Session, user_id: str):
    user = db.query(models.User).get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
