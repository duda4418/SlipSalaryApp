from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from datetime import datetime, timezone
from db import models

__all__ = [
    'repo_create_idempotency_key',
    'repo_update_idempotency_key',
    'repo_delete_idempotency_key',
    'repo_list_idempotency_keys',
    'repo_get_idempotency_key_by_id',
    'repo_get_idempotency_key_by_key',
    'repo_mark_idempotency_key_succeeded',
]

def repo_create_idempotency_key(db: Session, **data):
    key = models.IdempotencyKey(**data)
    db.add(key)
    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail="Idempotency key violates unique constraint") from e
    db.refresh(key)
    return key

def repo_update_idempotency_key(db: Session, key_id: str, **data):
    key = db.get(models.IdempotencyKey, key_id)
    if not key:
        raise HTTPException(status_code=404, detail="Idempotency key not found")
    for k, v in data.items():
        setattr(key, k, v)
    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail="Idempotency key violates unique constraint") from e
    db.refresh(key)
    return key

def repo_delete_idempotency_key(db: Session, key_id: str):
    key = db.get(models.IdempotencyKey, key_id)
    if not key:
        raise HTTPException(status_code=404, detail="Idempotency key not found")
    db.delete(key)
    db.commit()
    return {"deleted": True, "id": key_id}

def repo_list_idempotency_keys(db: Session):
    return db.query(models.IdempotencyKey).all()

def repo_get_idempotency_key_by_id(db: Session, key_id: str):
    key = db.get(models.IdempotencyKey, key_id)
    if not key:
        raise HTTPException(status_code=404, detail="Idempotency key not found")
    return key

def repo_get_idempotency_key_by_key(db: Session, key: str):
    return db.query(models.IdempotencyKey).filter(models.IdempotencyKey.key == key).first()

def repo_mark_idempotency_key_succeeded(db: Session, key_obj: models.IdempotencyKey, result_path: str | None = None):
    key_obj.status = 'succeeded'
    if result_path:
        key_obj.result_path = result_path
    key_obj.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(key_obj)
    return key_obj
