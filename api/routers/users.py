from fastapi import APIRouter


users_router = APIRouter(prefix="/users")

@users_router.get("")
def list_users():
    pass

@users_router.get("/{user_id}")
def get_user(user_id: str):
    pass

@users_router.post("")
def create_user():
    pass

@users_router.put("/{user_id}")
def update_user(user_id: str):
    pass

@users_router.delete("/{user_id}")
def delete_user(user_id: str):
    pass

