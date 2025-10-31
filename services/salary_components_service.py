from sqlalchemy.orm import Session
from db.repositories import (
    repo_list_salary_components,
    repo_get_salary_component_by_id,
    repo_create_salary_component,
    repo_update_salary_component,
    repo_delete_salary_component,
)
from api.schemas import SalaryComponentCreate, SalaryComponentUpdate


def get_salary_components(db: Session):
    return repo_list_salary_components(db)


def get_salary_component_by_id(db: Session, component_id: str):
    return repo_get_salary_component_by_id(db, component_id)


def create_salary_component(db: Session, component_in: SalaryComponentCreate):
    data = component_in.model_dump()
    return repo_create_salary_component(db, **data)


def update_salary_component(db: Session, component_id: str, patch: SalaryComponentUpdate):
    update_data = patch.model_dump(exclude_unset=True)
    return repo_update_salary_component(db, component_id, **update_data)


def delete_salary_component(db: Session, component_id: str):
    return repo_delete_salary_component(db, component_id)
