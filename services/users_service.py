from sqlalchemy.orm import Session
from db.repositories import (
    repo_list_users,
    repo_get_user_by_id,
    repo_create_user,
    repo_update_user,
    repo_delete_user,
)

def get_users(db: Session):
    return repo_list_users(db)

def get_user_by_id(db: Session, user_id: str):
    return repo_get_user_by_id(db, user_id)

def create_user(db: Session, data: dict):
    return repo_create_user(db, **data)

def update_user(db: Session, user_id: str, data: dict):
    return repo_update_user(db, user_id, **data)

def delete_user(db: Session, user_id: str):
    return repo_delete_user(db, user_id)
