
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import session
from api.schemas import UserResponse
from services.users_service import get_users as svc_list_users
from services.users_service import get_user_by_id as svc_get_user_by_id

users_router = APIRouter(prefix="/users")

@users_router.get("", response_model=list[UserResponse])
def list_users(db: Session = Depends(session.get_db)):
    return svc_list_users(db)

@users_router.get("/{user_id}", response_model=UserResponse)
def get_user_by_id_endpoint(user_id: str, db: Session = Depends(session.get_db)):
    return svc_get_user_by_id(db, user_id)

@users_router.post("")
def create_user():
    pass

@users_router.put("/{user_id}")
def update_user(user_id: str):
    pass

@users_router.delete("/{user_id}")
def delete_user(user_id: str):
    pass

