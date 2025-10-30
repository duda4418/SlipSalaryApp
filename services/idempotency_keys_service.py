from sqlalchemy.orm import Session
from db import models
from fastapi import HTTPException

def get_idempotency_keys(db: Session):
    return db.query(models.IdempotencyKey).all()

def get_idempotency_key_by_id(db: Session, key_id: str):
    key = db.query(models.IdempotencyKey).get(key_id)
    if not key:
        raise HTTPException(status_code=404, detail="Idempotency key not found")
    return key
