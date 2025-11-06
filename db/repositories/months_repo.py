from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from db import models

__all__ = [
    'repo_create_month',
    'repo_update_month',
    'repo_delete_month',
    'repo_list_months',
    'repo_get_month_by_id',
    'repo_get_month_info_by_year_month',
]

def repo_create_month(db: Session, **data):
    month = models.MonthInfo(**data)
    db.add(month)
    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail="Month violates unique constraint") from e
    db.refresh(month)
    return month

def repo_update_month(db: Session, month_id: str, **data):
    month = db.get(models.MonthInfo, month_id)
    if not month:
        raise HTTPException(status_code=404, detail="Month not found")
    for k, v in data.items():
        setattr(month, k, v)
    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail="Month violates unique constraint") from e
    db.refresh(month)
    return month

def repo_delete_month(db: Session, month_id: str):
    month = db.get(models.MonthInfo, month_id)
    if not month:
        raise HTTPException(status_code=404, detail="Month not found")
    db.delete(month)
    db.commit()
    return {"deleted": True, "id": month_id}

def repo_list_months(db: Session):
    return db.query(models.MonthInfo).all()

def repo_get_month_by_id(db: Session, month_id: str):
    month = db.get(models.MonthInfo, month_id)
    if not month:
        raise HTTPException(status_code=404, detail="Month not found")
    return month

def repo_get_month_info_by_year_month(db: Session, year: int, month: int):
    mi = db.query(models.MonthInfo).filter(models.MonthInfo.year == year, models.MonthInfo.month == month).first()
    if not mi:
        raise HTTPException(status_code=400, detail="Month info not defined")
    return mi
