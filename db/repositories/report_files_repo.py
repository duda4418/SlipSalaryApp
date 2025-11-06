from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from db import models

__all__ = [
    'repo_create_report_file',
    'repo_update_report_file',
    'repo_delete_report_file',
    'repo_list_report_files',
    'repo_get_report_file_by_id',
    'repo_get_report_file_by_path',
]

def repo_create_report_file(db: Session, **data):
    """Create or update a ReportFile for a given path to prevent duplicate rows."""
    path = data.get('path')
    existing = None
    if path:
        existing = db.query(models.ReportFile).filter(models.ReportFile.path == path).first()
    content = data.get('content')
    if existing:
        if content is not None:
            existing.content = content
            existing.size_bytes = len(content)
            ctype = data.get('content_type')
            if ctype:
                existing.content_type = ctype
            elif not existing.content_type:
                ftype = data.get('type', existing.type)
                mime_map = {'csv': 'text/csv', 'pdf': 'application/pdf', 'zip': 'application/zip'}
                existing.content_type = mime_map.get(ftype, 'application/octet-stream')
        for field in ['type','owner_id','archived']:
            if field in data and getattr(existing, field) != data[field]:
                setattr(existing, field, data[field])
        try:
            db.commit()
        except IntegrityError as e:
            db.rollback()
            raise HTTPException(status_code=400, detail="Report file violates unique constraint") from e
        db.refresh(existing)
        return existing
    if content is not None:
        data.setdefault('size_bytes', len(content))
        if 'content_type' not in data or data['content_type'] is None:
            ftype = data.get('type')
            mime_map = {'csv': 'text/csv', 'pdf': 'application/pdf', 'zip': 'application/zip'}
            data['content_type'] = mime_map.get(ftype, 'application/octet-stream')
    report = models.ReportFile(**data)
    db.add(report)
    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail="Report file violates unique constraint") from e
    db.refresh(report)
    return report

def repo_update_report_file(db: Session, report_id: str, **data):
    report = db.get(models.ReportFile, report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    for k, v in data.items():
        setattr(report, k, v)
    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail="Report file violates unique constraint") from e
    db.refresh(report)
    return report

def repo_delete_report_file(db: Session, report_id: str):
    report = db.get(models.ReportFile, report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    db.delete(report)
    db.commit()
    return {"deleted": True, "id": report_id}

def repo_list_report_files(db: Session):
    return db.query(models.ReportFile).all()

def repo_get_report_file_by_id(db: Session, report_id: str):
    report = db.get(models.ReportFile, report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    return report

def repo_get_report_file_by_path(db: Session, path: str):
    return db.query(models.ReportFile).filter(models.ReportFile.path == path).first()
