from fastapi import APIRouter, Depends
from auth.deps import require_manager
from sqlalchemy.orm import Session
from db import session
from api.schemas import IdempotencyKeyResponse, IdempotencyKeyCreate, IdempotencyKeyUpdate
from services.idempotency_keys_service import (
    get_idempotency_keys as svc_list_idempotency_keys,
    get_idempotency_key_by_id as svc_get_idempotency_key_by_id,
    create_idempotency_key as svc_create_idempotency_key,
    update_idempotency_key as svc_update_idempotency_key,
    delete_idempotency_key as svc_delete_idempotency_key,
)

idempotency_router = APIRouter(prefix="/idempotency_keys", dependencies=[Depends(require_manager)])


@idempotency_router.get("", response_model=list[IdempotencyKeyResponse])
def list_idempotency_keys(db: Session = Depends(session.get_db)):
    return svc_list_idempotency_keys(db)


@idempotency_router.get("/{key_id}", response_model=IdempotencyKeyResponse)
def get_idempotency_key_by_id(key_id: str, db: Session = Depends(session.get_db)):
    return svc_get_idempotency_key_by_id(db, key_id)


@idempotency_router.post("", response_model=IdempotencyKeyResponse)
def create_idempotency_key(key: IdempotencyKeyCreate, db: Session = Depends(session.get_db)):
    return svc_create_idempotency_key(db, key)


@idempotency_router.put("/{key_id}", response_model=IdempotencyKeyResponse)
def update_idempotency_key(key_id: str, key: IdempotencyKeyUpdate, db: Session = Depends(session.get_db)):
    return svc_update_idempotency_key(db, key_id, key)


@idempotency_router.delete("/{key_id}")
def delete_idempotency_key(key_id: str, db: Session = Depends(session.get_db)):
    return svc_delete_idempotency_key(db, key_id)
