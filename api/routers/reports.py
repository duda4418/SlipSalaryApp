from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import session
from api.schemas import ReportFileResponse
from services.reports_service import get_report_files as svc_list_report_files
from services.reports_service import get_report_file_by_id as svc_get_report_file_by_id

reports_router = APIRouter(prefix="/reports")

@reports_router.get("", response_model=list[ReportFileResponse])
def list_report_files(db: Session = Depends(session.get_db)):
    return svc_list_report_files(db)

@reports_router.get("/{report_id}", response_model=ReportFileResponse)
def get_report_file_by_id_endpoint(report_id: str, db: Session = Depends(session.get_db)):
    return svc_get_report_file_by_id(db, report_id)


@reports_router.post("")
def create_report_file():
    pass

@reports_router.put("/{report_id}")
def update_report_file(report_id: str):
    pass

@reports_router.delete("/{report_id}")
def delete_report_file(report_id: str):
    pass
