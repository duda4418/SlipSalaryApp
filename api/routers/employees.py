from fastapi import APIRouter

employees_router = APIRouter(prefix="/employees")

@employees_router.get("")
def list_employees():
    pass

@employees_router.get("/{employee_id}")
def get_employee(employee_id: str):
    pass

@employees_router.post("")
def create_employee():
    pass

@employees_router.put("/{employee_id}")
def update_employee(employee_id: str):
    pass

@employees_router.delete("/{employee_id}")
def delete_employee(employee_id: str):
    pass
