from sqlalchemy.orm import Session
from db.repositories import (
    repo_list_report_files,
    repo_get_report_file_by_id,
    repo_create_report_file,
    repo_update_report_file,
    repo_delete_report_file,
)

def get_report_files(db: Session):
    return repo_list_report_files(db)

def get_report_file_by_id(db: Session, report_id: str):
    return repo_get_report_file_by_id(db, report_id)

def create_report_file(db: Session, data: dict):
    return repo_create_report_file(db, **data)

def update_report_file(db: Session, report_id: str, data: dict):
    return repo_update_report_file(db, report_id, **data)

def delete_report_file(db: Session, report_id: str):
    return repo_delete_report_file(db, report_id)
