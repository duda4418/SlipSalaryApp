from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import models, session

reports_router = APIRouter(prefix="/reports")

@reports_router.get("")
def list_report_files(db: Session = Depends(session.get_db)):
    return db.query(models.ReportFile).all()

@reports_router.get("/{report_id}")
def get_report_file_by_id(report_id: str, db: Session = Depends(session.get_db)):
    report = db.query(models.ReportFile).get(report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    return report

@reports_router.post("")
def create_report_file():
    pass

@reports_router.put("/{report_id}")
def update_report_file(report_id: str):
    pass

@reports_router.delete("/{report_id}")
def delete_report_file(report_id: str):
    pass
