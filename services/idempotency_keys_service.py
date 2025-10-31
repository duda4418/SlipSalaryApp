from sqlalchemy.orm import Session
from db.repositories import (
    repo_list_idempotency_keys,
    repo_get_idempotency_key_by_id,
    repo_create_idempotency_key,
    repo_update_idempotency_key,
    repo_delete_idempotency_key,
)

def get_idempotency_keys(db: Session):
    return repo_list_idempotency_keys(db)

def get_idempotency_key_by_id(db: Session, key_id: str):
    return repo_get_idempotency_key_by_id(db, key_id)

def create_idempotency_key(db: Session, data: dict):
    return repo_create_idempotency_key(db, **data)

def update_idempotency_key(db: Session, key_id: str, data: dict):
    return repo_update_idempotency_key(db, key_id, **data)

def delete_idempotency_key(db: Session, key_id: str):
    return repo_delete_idempotency_key(db, key_id)
