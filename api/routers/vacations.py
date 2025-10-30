from fastapi import APIRouter

vacation_router = APIRouter(prefix="/vacations")

@vacation_router.get("")
def list_vacations():
    pass

@vacation_router.get("/{vacation_id}")
def get_vacation(vacation_id: str):
    pass

@vacation_router.post("")
def create_vacation():
    pass

@vacation_router.put("/{vacation_id}")
def update_vacation(vacation_id: str):
    pass

@vacation_router.delete("/{vacation_id}")
def delete_vacation(vacation_id: str):
    pass
