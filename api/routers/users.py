
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import models, session
from api.schemas import UserResponse

users_router = APIRouter(prefix="/users")

@users_router.get("", response_model=list[UserResponse])
def list_users(db: Session = Depends(session.get_db)):
    return db.query(models.User).all()

@users_router.get("/{user_id}", response_model=UserResponse)
def get_user_by_id(user_id: str, db: Session = Depends(session.get_db)):
    user = db.query(models.User).get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@users_router.post("")
def create_user():
    pass

@users_router.put("/{user_id}")
def update_user(user_id: str):
    pass

@users_router.delete("/{user_id}")
def delete_user(user_id: str):
    pass

