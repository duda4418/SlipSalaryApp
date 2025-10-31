from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db import session
from api.schemas import MonthInfoResponse, MonthInfoCreate, MonthInfoUpdate
from services.months_service import (
    get_months as svc_list_months,
    get_month_by_id as svc_get_month_by_id,
    create_month as svc_create_month,
    update_month as svc_update_month,
    delete_month as svc_delete_month,
)

months_router = APIRouter(prefix="/months")


@months_router.get("", response_model=list[MonthInfoResponse])
def list_months(db: Session = Depends(session.get_db)):
    return svc_list_months(db)


@months_router.get("/{month_id}", response_model=MonthInfoResponse)
def get_month_by_id_endpoint(month_id: str, db: Session = Depends(session.get_db)):
    return svc_get_month_by_id(db, month_id)


@months_router.post("", response_model=MonthInfoResponse)
def create_month_endpoint(month: MonthInfoCreate, db: Session = Depends(session.get_db)):
    return svc_create_month(db, month)


@months_router.put("/{month_id}", response_model=MonthInfoResponse)
def update_month_endpoint(month_id: str, month: MonthInfoUpdate, db: Session = Depends(session.get_db)):
    return svc_update_month(db, month_id, month)


@months_router.delete("/{month_id}")
def delete_month_endpoint(month_id: str, db: Session = Depends(session.get_db)):
    return svc_delete_month(db, month_id)
