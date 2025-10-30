from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import session
from api.schemas import IdempotencyKeyResponse
from services.idempotency_keys_service import get_idempotency_keys as svc_list_idempotency_keys
from services.idempotency_keys_service import get_idempotency_key_by_id as svc_get_idempotency_key_by_id

idempotency_router = APIRouter(prefix="/idempotency_keys")

@idempotency_router.get("", response_model=list[IdempotencyKeyResponse])
def list_idempotency_keys(db: Session = Depends(session.get_db)):
    return svc_list_idempotency_keys(db)

@idempotency_router.get("/{key_id}", response_model=IdempotencyKeyResponse)
def get_idempotency_key_by_id_endpoint(key_id: str, db: Session = Depends(session.get_db)):
    return svc_get_idempotency_key_by_id(db, key_id)

@idempotency_router.post("")
def create_idempotency_key():
    pass

@idempotency_router.put("/{key_id}")
def update_idempotency_key(key_id: str):
    pass

@idempotency_router.delete("/{key_id}")
def delete_idempotency_key(key_id: str):
    pass
