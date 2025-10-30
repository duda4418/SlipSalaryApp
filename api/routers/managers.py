from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import models, session

managers_router = APIRouter(prefix="/managers")

@managers_router.get("")
def list_managers(db: Session = Depends(session.get_db)):
    return db.query(models.Manager).all()

@managers_router.get("/{manager_id}")
def get_manager_by_id(manager_id: str, db: Session = Depends(session.get_db)):
    manager = db.query(models.Manager).get(manager_id)
    if not manager:
        raise HTTPException(status_code=404, detail="Manager not found")
    return manager

@managers_router.post("")
def create_manager():
    pass

@managers_router.put("/{manager_id}")
def update_manager(manager_id: str):
    pass

@managers_router.delete("/{manager_id}")
def delete_manager(manager_id: str):
    pass
