from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import session
from api.schemas import MonthInfoResponse
from services.months_service import get_months as svc_list_months
from services.months_service import get_month_by_id as svc_get_month_by_id

months_router = APIRouter(prefix="/months")

@months_router.get("", response_model=list[MonthInfoResponse])
def list_months(db: Session = Depends(session.get_db)):
    return svc_list_months(db)

@months_router.get("/{month_id}", response_model=MonthInfoResponse)
def get_month_by_id_endpoint(month_id: str, db: Session = Depends(session.get_db)):
    return svc_get_month_by_id(db, month_id)

@months_router.post("")
def create_month():
    pass

@months_router.put("/{month_id}")
def update_month(month_id: str):
    pass

@months_router.delete("/{month_id}")
def delete_month(month_id: str):
    pass
