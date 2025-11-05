from sqlalchemy.orm import Session
from db.repositories import (
    repo_list_employees,
    repo_get_employee_by_id,
    repo_create_employee,
    repo_update_employee,
    repo_delete_employee,
    repo_get_employees_by_manager,
)
from api.schemas import EmployeeCreate, EmployeeUpdate


def get_employees(db: Session):
    return repo_list_employees(db)

def get_employees_by_manager(db: Session, manager_id: str):
    return repo_get_employees_by_manager(db, manager_id)


def get_employee_by_id(db: Session, employee_id: str):
    return repo_get_employee_by_id(db, employee_id)


def create_employee(db: Session, employee_in: EmployeeCreate):
    data = employee_in.model_dump()
    return repo_create_employee(db, **data)


def update_employee(db: Session, employee_id: str, patch: EmployeeUpdate):
    update_data = patch.model_dump(exclude_unset=True)
    return repo_update_employee(db, employee_id, **update_data)


def delete_employee(db: Session, employee_id: str):
    return repo_delete_employee(db, employee_id)
