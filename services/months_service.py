from sqlalchemy.orm import Session
from db.repositories import (
    repo_list_months,
    repo_get_month_by_id,
    repo_create_month,
    repo_update_month,
    repo_delete_month,
)
from api.schemas import MonthInfoCreate, MonthInfoUpdate


def get_months(db: Session):
    return repo_list_months(db)


def get_month_by_id(db: Session, month_id: str):
    return repo_get_month_by_id(db, month_id)


def create_month(db: Session, month_in: MonthInfoCreate):
    data = month_in.model_dump()
    return repo_create_month(db, **data)


def update_month(db: Session, month_id: str, patch: MonthInfoUpdate):
    update_data = patch.model_dump(exclude_unset=True)
    return repo_update_month(db, month_id, **update_data)


def delete_month(db: Session, month_id: str):
    return repo_delete_month(db, month_id)
