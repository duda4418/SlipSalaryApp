from fastapi import HTTPException
from sqlalchemy.orm import Session
from db import models

def get_vacations(db: Session):
    return db.query(models.Vacation).all()

def get_vacation_by_id(db: Session, vacation_id: str):
    vacation = db.query(models.Vacation).get(vacation_id)
    if not vacation:
        raise HTTPException(status_code=404, detail="Vacation not found")
    return vacation
