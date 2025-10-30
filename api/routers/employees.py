from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import models, session
from api.schemas import EmployeeResponse

employees_router = APIRouter(prefix="/employees")

@employees_router.get("", response_model=list[EmployeeResponse])
def list_employees(db: Session = Depends(session.get_db)):
    return db.query(models.Employee).all()

@employees_router.get("/{employee_id}", response_model=EmployeeResponse)
def get_employee_by_id(employee_id: str, db: Session = Depends(session.get_db)):
    employee = db.query(models.Employee).get(employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee

@employees_router.post("")
def create_employee():
    pass

@employees_router.put("/{employee_id}")
def update_employee(employee_id: str):
    pass

@employees_router.delete("/{employee_id}")
def delete_employee(employee_id: str):
    pass
