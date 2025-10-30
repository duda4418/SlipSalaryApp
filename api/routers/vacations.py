from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import session
from api.schemas import VacationResponse
from services.vacations_service import get_vacations as svc_list_vacations
from services.vacations_service import get_vacation_by_id as svc_get_vacation_by_id

vacations_router = APIRouter(prefix="/vacations")

@vacations_router.get("", response_model=list[VacationResponse])
def list_vacations(db: Session = Depends(session.get_db)):
    return svc_list_vacations(db)

@vacations_router.get("/{vacation_id}", response_model=VacationResponse)
def get_vacation_by_id_endpoint(vacation_id: str, db: Session = Depends(session.get_db)):
    return svc_get_vacation_by_id(db, vacation_id)

@vacations_router.post("")
def create_vacation():
    pass

@vacations_router.put("/{vacation_id}")
def update_vacation(vacation_id: str):
    pass

@vacations_router.delete("/{vacation_id}")
def delete_vacation(vacation_id: str):
    pass
