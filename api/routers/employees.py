from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db import session
from api.schemas import EmployeeResponse
from services.employees_service import get_employees as svc_list_employees
from services.employees_service import get_employee_by_id as svc_get_employee_by_id

employees_router = APIRouter(prefix="/employees")

@employees_router.get("", response_model=list[EmployeeResponse])
def list_employees(db: Session = Depends(session.get_db)):
    return svc_list_employees(db)

@employees_router.get("/{employee_id}", response_model=EmployeeResponse)
def get_employee_by_id_endpoint(employee_id: str, db: Session = Depends(session.get_db)):
    return svc_get_employee_by_id(db, employee_id)

@employees_router.post("")
def create_employee():
    pass

@employees_router.put("/{employee_id}")
def update_employee(employee_id: str):
    pass

@employees_router.delete("/{employee_id}")
def delete_employee(employee_id: str):
    pass
