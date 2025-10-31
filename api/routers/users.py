
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import session
from api.schemas import UserResponse, UserCreate, UserUpdate
from services.users_service import (
    get_users as svc_list_users,
    get_user_by_id as svc_get_user_by_id,
    create_user as svc_create_user,
    update_user as svc_update_user,
    delete_user as svc_delete_user,
)

users_router = APIRouter(prefix="/users")

@users_router.get("", response_model=list[UserResponse])
def list_users(db: Session = Depends(session.get_db)):
    return svc_list_users(db)

@users_router.get("/{user_id}", response_model=UserResponse)
def get_user_by_id_endpoint(user_id: str, db: Session = Depends(session.get_db)):
    return svc_get_user_by_id(db, user_id)

@users_router.post("", response_model=UserResponse)
def create_user_endpoint(payload: UserCreate, db: Session = Depends(session.get_db)):
    user = svc_create_user(db, payload.model_dump())
    return user

@users_router.put("/{user_id}", response_model=UserResponse)
def update_user_endpoint(user_id: str, payload: UserUpdate, db: Session = Depends(session.get_db)):
    data = {k: v for k, v in payload.model_dump().items() if v is not None}
    user = svc_update_user(db, user_id, data)
    return user

@users_router.delete("/{user_id}")
def delete_user_endpoint(user_id: str, db: Session = Depends(session.get_db)):
    return svc_delete_user(db, user_id)

