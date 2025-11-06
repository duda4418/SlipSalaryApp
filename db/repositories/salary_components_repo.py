from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from db import models

__all__ = [
    'repo_create_salary_component',
    'repo_update_salary_component',
    'repo_delete_salary_component',
    'repo_list_salary_components',
    'repo_get_salary_component_by_id',
]

def repo_create_salary_component(db: Session, **data):
    component = models.SalaryComponent(**data)
    db.add(component)
    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail="Salary component violates unique constraint") from e
    db.refresh(component)
    return component

def repo_update_salary_component(db: Session, component_id: str, **data):
    component = db.get(models.SalaryComponent, component_id)
    if not component:
        raise HTTPException(status_code=404, detail="Salary component not found")
    for k, v in data.items():
        setattr(component, k, v)
    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail="Salary component violates unique constraint") from e
    db.refresh(component)
    return component

def repo_delete_salary_component(db: Session, component_id: str):
    component = db.get(models.SalaryComponent, component_id)
    if not component:
        raise HTTPException(status_code=404, detail="Salary component not found")
    db.delete(component)
    db.commit()
    return {"deleted": True, "id": component_id}

def repo_list_salary_components(db: Session):
    return db.query(models.SalaryComponent).all()

def repo_get_salary_component_by_id(db: Session, component_id: str):
    component = db.get(models.SalaryComponent, component_id)
    if not component:
        raise HTTPException(status_code=404, detail="Salary component not found")
    return component
