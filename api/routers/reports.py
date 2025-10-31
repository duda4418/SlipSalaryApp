from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import session
from api.schemas import ReportFileResponse, ReportFileCreate, ReportFileUpdate
from services.reports_service import (
    get_report_files as svc_list_report_files,
    get_report_file_by_id as svc_get_report_file_by_id,
    create_report_file as svc_create_report_file,
    update_report_file as svc_update_report_file,
    delete_report_file as svc_delete_report_file,
)

reports_router = APIRouter(prefix="/reports")

@reports_router.get("", response_model=list[ReportFileResponse])
def list_report_files(db: Session = Depends(session.get_db)):
    return svc_list_report_files(db)

@reports_router.get("/{report_id}", response_model=ReportFileResponse)
def get_report_file_by_id_endpoint(report_id: str, db: Session = Depends(session.get_db)):
    return svc_get_report_file_by_id(db, report_id)


@reports_router.post("", response_model=ReportFileResponse)
def create_report_file_endpoint(payload: ReportFileCreate, db: Session = Depends(session.get_db)):
    report = svc_create_report_file(db, payload.model_dump())
    return report

@reports_router.put("/{report_id}", response_model=ReportFileResponse)
def update_report_file_endpoint(report_id: str, payload: ReportFileUpdate, db: Session = Depends(session.get_db)):
    data = {k: v for k, v in payload.model_dump().items() if v is not None}
    report = svc_update_report_file(db, report_id, data)
    return report

@reports_router.delete("/{report_id}")
def delete_report_file_endpoint(report_id: str, db: Session = Depends(session.get_db)):
    return svc_delete_report_file(db, report_id)
