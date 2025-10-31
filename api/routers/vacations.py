from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import session
from api.schemas import VacationResponse, VacationCreate, VacationUpdate
from services.vacations_service import (
    get_vacations as svc_list_vacations,
    get_vacation_by_id as svc_get_vacation_by_id,
    create_vacation as svc_create_vacation,
    update_vacation as svc_update_vacation,
    delete_vacation as svc_delete_vacation,
)

vacations_router = APIRouter(prefix="/vacations")

@vacations_router.get("", response_model=list[VacationResponse])
def list_vacations(db: Session = Depends(session.get_db)):
    return svc_list_vacations(db)

@vacations_router.get("/{vacation_id}", response_model=VacationResponse)
def get_vacation_by_id_endpoint(vacation_id: str, db: Session = Depends(session.get_db)):
    return svc_get_vacation_by_id(db, vacation_id)

@vacations_router.post("", response_model=VacationResponse)
def create_vacation_endpoint(payload: VacationCreate, db: Session = Depends(session.get_db)):
    vacation = svc_create_vacation(db, payload.model_dump())
    return vacation

@vacations_router.put("/{vacation_id}", response_model=VacationResponse)
def update_vacation_endpoint(vacation_id: str, payload: VacationUpdate, db: Session = Depends(session.get_db)):
    data = {k: v for k, v in payload.model_dump().items() if v is not None}
    vacation = svc_update_vacation(db, vacation_id, data)
    return vacation

@vacations_router.delete("/{vacation_id}")
def delete_vacation_endpoint(vacation_id: str, db: Session = Depends(session.get_db)):
    return svc_delete_vacation(db, vacation_id)
