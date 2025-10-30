from sqlalchemy.orm import Session
from db import models
from fastapi import HTTPException

def get_months(db: Session):
    return db.query(models.MonthInfo).all()

def get_month_by_id(db: Session, month_id: str):
    month = db.query(models.MonthInfo).get(month_id)
    if not month:
        raise HTTPException(status_code=404, detail="Month not found")
    return month
