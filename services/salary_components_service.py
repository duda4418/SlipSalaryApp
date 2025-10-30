from fastapi import HTTPException
from sqlalchemy.orm import Session
from db import models

def get_salary_components(db: Session):
    return db.query(models.SalaryComponent).all()

def get_salary_component_by_id(db: Session, component_id: str):
    component = db.query(models.SalaryComponent).get(component_id)
    if not component:
        raise HTTPException(status_code=404, detail="Salary component not found")
    return component
