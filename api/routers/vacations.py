from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import models, session
from api.schemas import VacationResponse

vacations_router = APIRouter(prefix="/vacations")

@vacations_router.get("", response_model=list[VacationResponse])
def list_vacations(db: Session = Depends(session.get_db)):
    return db.query(models.Vacation).all()

@vacations_router.get("/{vacation_id}", response_model=VacationResponse)
def get_vacation_by_id(vacation_id: str, db: Session = Depends(session.get_db)):
    vacation = db.query(models.Vacation).get(vacation_id)
    if not vacation:
        raise HTTPException(status_code=404, detail="Vacation not found")
    return vacation

@vacations_router.post("")
def create_vacation():
    pass

@vacations_router.put("/{vacation_id}")
def update_vacation(vacation_id: str):
    pass

@vacations_router.delete("/{vacation_id}")
def delete_vacation(vacation_id: str):
    pass
