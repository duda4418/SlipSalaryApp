from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from db import models

__all__ = [
    'repo_list_employees',
    'repo_get_employees_by_manager',
    'repo_get_employee_by_email',
    'repo_get_employee_by_id',
    'repo_create_employee',
    'repo_update_employee',
    'repo_delete_employee',
]

def repo_list_employees(db: Session):
    return db.query(models.Employee).all()

def repo_get_employees_by_manager(db: Session, manager_id: str):
    """Return all employees managed by the given manager (excludes manager themselves)."""
    return db.query(models.Employee).filter(models.Employee.manager_id == manager_id).all()

def repo_get_employee_by_email(db: Session, email: str):
    return db.query(models.Employee).filter(models.Employee.email == email).first()

def repo_get_employee_by_id(db: Session, employee_id: str):
    employee = db.get(models.Employee, employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee

def repo_create_employee(db: Session, **data):
    employee = models.Employee(**data)
    db.add(employee)
    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail="Employee violates unique constraint") from e
    db.refresh(employee)
    return employee

def repo_update_employee(db: Session, employee_id: str, **data):
    employee = db.get(models.Employee, employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    for key, value in data.items():
        setattr(employee, key, value)
    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail="Employee violates unique constraint") from e
    db.refresh(employee)
    return employee

def repo_delete_employee(db: Session, employee_id: str):
    employee = db.get(models.Employee, employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    db.delete(employee)
    db.commit()
    return {"deleted": True, "id": employee_id}
