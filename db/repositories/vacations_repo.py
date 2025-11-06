from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from db import models

__all__ = [
    'repo_create_vacation',
    'repo_update_vacation',
    'repo_delete_vacation',
    'repo_list_vacations',
    'repo_get_vacation_by_id',
]

def repo_create_vacation(db: Session, **data):
    vacation = models.Vacation(**data)
    db.add(vacation)
    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail="Vacation violates unique constraint") from e
    db.refresh(vacation)
    return vacation

def repo_update_vacation(db: Session, vacation_id: str, **data):
    vacation = db.get(models.Vacation, vacation_id)
    if not vacation:
        raise HTTPException(status_code=404, detail="Vacation not found")
    for k, v in data.items():
        setattr(vacation, k, v)
    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail="Vacation violates unique constraint") from e
    db.refresh(vacation)
    return vacation

def repo_delete_vacation(db: Session, vacation_id: str):
    vacation = db.get(models.Vacation, vacation_id)
    if not vacation:
        raise HTTPException(status_code=404, detail="Vacation not found")
    db.delete(vacation)
    db.commit()
    return {"deleted": True, "id": vacation_id}

def repo_list_vacations(db: Session):
    return db.query(models.Vacation).all()

def repo_get_vacation_by_id(db: Session, vacation_id: str):
    vacation = db.get(models.Vacation, vacation_id)
    if not vacation:
        raise HTTPException(status_code=404, detail="Vacation not found")
    return vacation
