from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse, FileResponse
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
import os

reports_router = APIRouter(prefix="/reports")


def _normalize_report_id(raw: str) -> str:
    """Strip an optional extension (.pdf/.csv/.zip) after the UUID so links like
    /reports/<uuid>.pdf work seamlessly. Returns the bare UUID part.
    """
    if not raw:
        return raw
    return raw.split('.', 1)[0]


@reports_router.get("", response_model=list[ReportFileResponse])
def list_report_files(db: Session = Depends(session.get_db)):
    return svc_list_report_files(db)


@reports_router.get("/{report_id}", response_model=ReportFileResponse)
def get_report_file_by_id_endpoint(report_id: str, db: Session = Depends(session.get_db)):
    clean_id = _normalize_report_id(report_id)
    return svc_get_report_file_by_id(db, clean_id)

@reports_router.get("/{report_id}/download")
def download_report_file(report_id: str, db: Session = Depends(session.get_db)):
    clean_id = _normalize_report_id(report_id)
    report = svc_get_report_file_by_id(db, clean_id)
    # Prefer inline DB content
    if getattr(report, 'content', None):
        media = report.content_type or 'application/octet-stream'
        filename = os.path.basename(report.path)
        return StreamingResponse(iter([report.content]), media_type=media, headers={
            'Content-Disposition': f'attachment; filename={filename}'
        })
    # Fallback to path on disk if content missing
    if not os.path.exists(report.path):
        raise HTTPException(status_code=404, detail='File not found')
    media_map = {'csv':'text/csv','pdf':'application/pdf','zip':'application/zip'}
    media = media_map.get(report.type, 'application/octet-stream')
    return FileResponse(report.path, media_type=media, filename=os.path.basename(report.path))


@reports_router.post("", response_model=ReportFileResponse)
def create_report_file_endpoint(report: ReportFileCreate, db: Session = Depends(session.get_db)):
    return svc_create_report_file(db, report)


@reports_router.put("/{report_id}", response_model=ReportFileResponse)
def update_report_file_endpoint(report_id: str, report: ReportFileUpdate, db: Session = Depends(session.get_db)):
    return svc_update_report_file(db, report_id, report)


@reports_router.delete("/{report_id}")
def delete_report_file_endpoint(report_id: str, db: Session = Depends(session.get_db)):
    return svc_delete_report_file(db, report_id)
