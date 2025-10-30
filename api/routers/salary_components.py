from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import models, session

salary_components_router = APIRouter(prefix="/salary_components")

@salary_components_router.get("")
def list_salary_components(db: Session = Depends(session.get_db)):
    return db.query(models.SalaryComponent).all()

@salary_components_router.get("/{component_id}")
def get_salary_component_by_id(component_id: str, db: Session = Depends(session.get_db)):
    component = db.query(models.SalaryComponent).get(component_id)
    if not component:
        raise HTTPException(status_code=404, detail="Salary component not found")
    return component

@salary_components_router.post("")
def create_salary_component():
    pass

@salary_components_router.put("/{component_id}")
def update_salary_component(component_id: str):
    pass

@salary_components_router.delete("/{component_id}")
def delete_salary_component(component_id: str):
    pass
