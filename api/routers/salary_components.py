from fastapi import APIRouter, Depends
from auth.deps import require_manager
from sqlalchemy.orm import Session
from db import session
from api.schemas import SalaryComponentResponse, SalaryComponentCreate, SalaryComponentUpdate
from services.salary_components_service import (
    get_salary_components as svc_list_salary_components,
    get_salary_component_by_id as svc_get_salary_component_by_id,
    create_salary_component as svc_create_salary_component,
    update_salary_component as svc_update_salary_component,
    delete_salary_component as svc_delete_salary_component,
)

salary_components_router = APIRouter(prefix="/salary_components", dependencies=[Depends(require_manager)])


@salary_components_router.get("", response_model=list[SalaryComponentResponse])
def list_salary_components(db: Session = Depends(session.get_db)):
    return svc_list_salary_components(db)


@salary_components_router.get("/{component_id}", response_model=SalaryComponentResponse)
def get_salary_component_by_id(component_id: str, db: Session = Depends(session.get_db)):
    return svc_get_salary_component_by_id(db, component_id)


@salary_components_router.post("", response_model=SalaryComponentResponse)
def create_salary_component(component: SalaryComponentCreate, db: Session = Depends(session.get_db)):
    return svc_create_salary_component(db, component)


@salary_components_router.put("/{component_id}", response_model=SalaryComponentResponse)
def update_salary_component(component_id: str, component: SalaryComponentUpdate, db: Session = Depends(session.get_db)):
    return svc_update_salary_component(db, component_id, component)


@salary_components_router.delete("/{component_id}")
def delete_salary_component(component_id: str, db: Session = Depends(session.get_db)):
    return svc_delete_salary_component(db, component_id)
