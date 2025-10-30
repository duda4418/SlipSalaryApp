from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import session
from api.schemas import SalaryComponentResponse
from services.salary_components_service import get_salary_components as svc_list_salary_components
from services.salary_components_service import get_salary_component_by_id as svc_get_salary_component_by_id

salary_components_router = APIRouter(prefix="/salary_components")

@salary_components_router.get("", response_model=list[SalaryComponentResponse])
def list_salary_components(db: Session = Depends(session.get_db)):
    return svc_list_salary_components(db)

@salary_components_router.get("/{component_id}", response_model=SalaryComponentResponse)
def get_salary_component_by_id_endpoint(component_id: str, db: Session = Depends(session.get_db)):
    return svc_get_salary_component_by_id(db, component_id)

@salary_components_router.post("")
def create_salary_component():
    pass

@salary_components_router.put("/{component_id}")
def update_salary_component(component_id: str):
    pass

@salary_components_router.delete("/{component_id}")
def delete_salary_component(component_id: str):
    pass
