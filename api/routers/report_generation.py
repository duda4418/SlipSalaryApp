from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session
from uuid import UUID
from db import session
from services.report_generation_service import (
    generate_manager_csv_idempotent,
    send_manager_csv,
    send_manager_csv_live,
    generate_employee_pdfs_idempotent,
    send_employee_pdfs,
    send_employee_pdfs_live,
)
from auth.deps import require_manager

report_generation_router = APIRouter(prefix="/reports_generation", tags=["reports-generation"])

@report_generation_router.post("/createAggregatedEmployeeData")
def create_aggregated_employee_data(managerId: UUID, year: int, month: int, includeBonuses: bool = True, idempotency_key: str | None = Header(default=None, alias="Idempotency-Key"), db: Session = Depends(session.get_db), _: None = Depends(require_manager)):
    return generate_manager_csv_idempotent(db, managerId, year, month, include_bonuses=includeBonuses, idempotency_key=idempotency_key)

@report_generation_router.post("/sendAggregatedEmployeeData")
def send_aggregated_employee_data(managerId: UUID, year: int, month: int, idempotency_key: str | None = Header(default=None, alias="Idempotency-Key"), db: Session = Depends(session.get_db), _: None = Depends(require_manager)):
    return send_manager_csv(db, managerId, year, month, idempotency_key=idempotency_key)

@report_generation_router.post("/sendAggregatedEmployeeDataLive")
def send_aggregated_employee_data_live(managerId: UUID, year: int, month: int, idempotency_key: str | None = Header(default=None, alias="Idempotency-Key"), db: Session = Depends(session.get_db), _: None = Depends(require_manager)):
    """Production variant of aggregated CSV email using real SMTP settings.

    Returns same structure as dev endpoint plus status 'sent_live'.
    """
    return send_manager_csv_live(db, managerId, year, month, idempotency_key=idempotency_key)

@report_generation_router.post("/createPdfForEmployees")
def create_pdf_for_employees(managerId: UUID, year: int, month: int, overwriteExisting: bool = False, idempotency_key: str | None = Header(default=None, alias="Idempotency-Key"), db: Session = Depends(session.get_db), _: None = Depends(require_manager)):
    return generate_employee_pdfs_idempotent(db, managerId, year, month, overwrite=overwriteExisting, idempotency_key=idempotency_key)

@report_generation_router.post("/sendPdfToEmployees")
def send_pdf_to_employees(managerId: UUID, year: int, month: int, regenerateMissing: bool = False, idempotency_key: str | None = Header(default=None, alias="Idempotency-Key"), db: Session = Depends(session.get_db), _: None = Depends(require_manager)):
    return send_employee_pdfs(db, managerId, year, month, regenerate_missing=regenerateMissing, idempotency_key=idempotency_key)

@report_generation_router.post("/sendPdfToEmployeesLive")
def send_pdf_to_employees_live(managerId: UUID, year: int, month: int, regenerateMissing: bool = False, idempotency_key: str | None = Header(default=None, alias="Idempotency-Key"), db: Session = Depends(session.get_db), _: None = Depends(require_manager)):
    """Send PDFs through real SMTP (non-local). Requires production SMTP settings configured.

    Returns same structure as the dev endpoint plus status flag 'sent_live'.
    """
    return send_employee_pdfs_live(db, managerId, year, month, regenerate_missing=regenerateMissing, idempotency_key=idempotency_key)
