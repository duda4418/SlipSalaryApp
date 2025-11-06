from sqlalchemy.orm import Session
from db.repositories.report_files_repo import (
    repo_list_report_files,
    repo_get_report_file_by_id,
    repo_create_report_file,
    repo_update_report_file,
    repo_delete_report_file,
)
from api.schemas import ReportFileCreate, ReportFileUpdate


def get_report_files(db: Session):
    return repo_list_report_files(db)


def get_report_file_by_id(db: Session, report_id: str):
    return repo_get_report_file_by_id(db, report_id)


def create_report_file(db: Session, report_in: ReportFileCreate):
    data = report_in.model_dump()
    return repo_create_report_file(db, **data)


def update_report_file(db: Session, report_id: str, patch: ReportFileUpdate):
    update_data = patch.model_dump(exclude_unset=True)
    return repo_update_report_file(db, report_id, **update_data)


def delete_report_file(db: Session, report_id: str):
    return repo_delete_report_file(db, report_id)
