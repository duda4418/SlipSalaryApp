from fastapi import APIRouter

managers_router = APIRouter(prefix="/managers")

@managers_router.get("")
def list_managers():
    pass

@managers_router.get("/{manager_id}")
def get_manager(manager_id: str):
    pass

@managers_router.post("")
def create_manager():
    pass

@managers_router.put("/{manager_id}")
def update_manager(manager_id: str):
    pass

@managers_router.delete("/{manager_id}")
def delete_manager(manager_id: str):
    pass
