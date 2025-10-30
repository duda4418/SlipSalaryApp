from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import models, session

months_router = APIRouter(prefix="/months")

@months_router.get("")
def list_months(db: Session = Depends(session.get_db)):
    return db.query(models.MonthInfo).all()

@months_router.get("/{month_id}")
def get_month_by_id(month_id: str, db: Session = Depends(session.get_db)):
    month = db.query(models.MonthInfo).get(month_id)
    if not month:
        raise HTTPException(status_code=404, detail="Month not found")
    return month

@months_router.post("")
def create_month():
    pass

@months_router.put("/{month_id}")
def update_month(month_id: str):
    pass

@months_router.delete("/{month_id}")
def delete_month(month_id: str):
    pass
