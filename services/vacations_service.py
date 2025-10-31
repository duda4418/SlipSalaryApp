from sqlalchemy.orm import Session
from db.repositories import (
    repo_list_vacations,
    repo_get_vacation_by_id,
    repo_create_vacation,
    repo_update_vacation,
    repo_delete_vacation,
)
from api.schemas import VacationCreate, VacationUpdate


def get_vacations(db: Session):
    return repo_list_vacations(db)


def get_vacation_by_id(db: Session, vacation_id: str):
    return repo_get_vacation_by_id(db, vacation_id)


def create_vacation(db: Session, vacation_in: VacationCreate):
    data = vacation_in.model_dump()
    return repo_create_vacation(db, **data)


def update_vacation(db: Session, vacation_id: str, patch: VacationUpdate):
    update_data = patch.model_dump(exclude_unset=True)
    return repo_update_vacation(db, vacation_id, **update_data)


def delete_vacation(db: Session, vacation_id: str):
    return repo_delete_vacation(db, vacation_id)
