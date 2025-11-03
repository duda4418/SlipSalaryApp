from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import UUID
from db import session
from services.report_generation_service import (
    generate_manager_csv,
    send_manager_csv,
    generate_employee_pdfs,
    send_employee_pdfs,
)
from auth.deps import require_manager

report_generation_router = APIRouter(prefix="/reports_generation", tags=["reports-generation"])

@report_generation_router.post("/createAggregatedEmployeeData")
def create_aggregated_employee_data(managerId: UUID, year: int, month: int, includeBonuses: bool = True, db: Session = Depends(session.get_db), _: None = Depends(require_manager)):
    report = generate_manager_csv(db, managerId, year, month, include_bonuses=includeBonuses)
    return {"fileId": str(report.id), "path": report.path, "archived": report.archived}

@report_generation_router.post("/sendAggregatedEmployeeData")
def send_aggregated_employee_data(managerId: UUID, year: int, month: int, db: Session = Depends(session.get_db), _: None = Depends(require_manager)):
    return send_manager_csv(db, managerId, year, month)

@report_generation_router.post("/createPdfForEmployees")
def create_pdf_for_employees(managerId: UUID, year: int, month: int, overwriteExisting: bool = False, db: Session = Depends(session.get_db), _: None = Depends(require_manager)):
    return generate_employee_pdfs(db, managerId, year, month, overwrite=overwriteExisting)

@report_generation_router.post("/sendPdfToEmployees")
def send_pdf_to_employees(managerId: UUID, year: int, month: int, regenerateMissing: bool = False, db: Session = Depends(session.get_db), _: None = Depends(require_manager)):
    return send_employee_pdfs(db, managerId, year, month, regenerate_missing=regenerateMissing)
