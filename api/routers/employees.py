from fastapi import APIRouter, Depends
from auth.deps import require_manager
from sqlalchemy.orm import Session
from db import session
from api.schemas import EmployeeResponse, EmployeeCreate, EmployeeUpdate
from services.employees_service import (
    get_employees as svc_list_employees,
    get_employee_by_id as svc_get_employee_by_id,
    create_employee as svc_create_employee,
    update_employee as svc_update_employee,
    delete_employee as svc_delete_employee,
)

employees_router = APIRouter(prefix="/employees", dependencies=[Depends(require_manager)])


@employees_router.get("", response_model=list[EmployeeResponse])
def list_employees(db: Session = Depends(session.get_db)):
    return svc_list_employees(db)


@employees_router.get("/{employee_id}", response_model=EmployeeResponse)
def get_employee_by_id_endpoint(employee_id: str, db: Session = Depends(session.get_db)):
    return svc_get_employee_by_id(db, employee_id)


@employees_router.post("", response_model=EmployeeResponse)
def create_employee_endpoint(employee: EmployeeCreate, db: Session = Depends(session.get_db)):
    return svc_create_employee(db, employee)


@employees_router.put("/{employee_id}", response_model=EmployeeResponse)
def update_employee_endpoint(employee_id: str, employee: EmployeeUpdate, db: Session = Depends(session.get_db)):
    return svc_update_employee(db, employee_id, employee)


@employees_router.delete("/{employee_id}")
def delete_employee_endpoint(employee_id: str, db: Session = Depends(session.get_db)):
    return svc_delete_employee(db, employee_id)
