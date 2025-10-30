from fastapi import APIRouter

months_router = APIRouter(prefix="/months")

@months_router.get("")
def list_months():
    pass

@months_router.get("/{month_id}")
def get_month(month_id: str):
    pass

@months_router.post("")
def create_month():
    pass

@months_router.put("/{month_id}")
def update_month(month_id: str):
    pass

@months_router.delete("/{month_id}")
def delete_month(month_id: str):
    pass
