from fastapi import APIRouter

idempotency_router = APIRouter(prefix="/idempotency-keys")

@idempotency_router.get("")
def list_idempotency_keys():
    pass

@idempotency_router.get("/{key_id}")
def get_idempotency_key(key_id: str):
    pass

@idempotency_router.post("")
def create_idempotency_key():
    pass

@idempotency_router.put("/{key_id}")
def update_idempotency_key(key_id: str):
    pass

@idempotency_router.delete("/{key_id}")
def delete_idempotency_key(key_id: str):
    pass
