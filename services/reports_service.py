from fastapi import HTTPException
from sqlalchemy.orm import Session
from db import models

def get_report_files(db: Session):
    return db.query(models.ReportFile).all()

def get_report_file_by_id(db: Session, report_id: str):
    report = db.query(models.ReportFile).get(report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    return report
