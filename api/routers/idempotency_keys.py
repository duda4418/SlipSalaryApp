from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import models, session
from api.schemas import IdempotencyKeyResponse

idempotency_router = APIRouter(prefix="/idempotency_keys")

@idempotency_router.get("", response_model=list[IdempotencyKeyResponse])
def list_idempotency_keys(db: Session = Depends(session.get_db)):
    return db.query(models.IdempotencyKey).all()

@idempotency_router.get("/{key_id}", response_model=IdempotencyKeyResponse)
def get_idempotency_key_by_id(key_id: str, db: Session = Depends(session.get_db)):
    key = db.query(models.IdempotencyKey).get(key_id)
    if not key:
        raise HTTPException(status_code=404, detail="Idempotency key not found")
    return key

@idempotency_router.post("")
def create_idempotency_key():
    pass

@idempotency_router.put("/{key_id}")
def update_idempotency_key(key_id: str):
    pass

@idempotency_router.delete("/{key_id}")
def delete_idempotency_key(key_id: str):
    pass
