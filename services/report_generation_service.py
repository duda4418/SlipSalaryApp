import os
from typing import List, Tuple
import shutil

from uuid import UUID
from sqlalchemy.orm import Session
from fastapi import HTTPException
from db import models
from db.repositories import (
    repo_create_report_file,
    repo_get_manager,
    repo_list_subordinates,
    repo_get_month_info_by_year_month,
    repo_aggregate_employee_month_summary,
    repo_update_report_file,
    repo_get_idempotency_key_by_key,
    repo_create_idempotency_key,
    repo_mark_idempotency_key_succeeded,
)
from utils.files import write_csv, zip_paths, ensure_dir
import mimetypes
from utils.pdf import build_salary_pdf
from services.email_service import send_email

BASE_REPORT_DIR = "reports"


def _get_manager(db: Session, manager_id: UUID) -> models.Employee:
    return repo_get_manager(db, str(manager_id))

def _get_subordinates(db: Session, manager_id: UUID) -> List[models.Employee]:
    return repo_list_subordinates(db, str(manager_id))

def _get_month_info(db: Session, year: int, month: int) -> models.MonthInfo:
    return repo_get_month_info_by_year_month(db, year, month)

def _get_summary(db: Session, manager_id: UUID, year: int, month: int):
    return repo_aggregate_employee_month_summary(db, str(manager_id), year, month)


def generate_manager_csv(db: Session, manager_id: UUID, year: int, month: int, include_bonuses: bool = True) -> models.ReportFile:
    manager = _get_manager(db, manager_id)
    subs = _get_subordinates(db, manager_id)
    month_info = _get_month_info(db, year, month)
    summary_rows = _get_summary(db, manager_id, year, month)

    headers = ["employee_id","first_name","last_name","cnp","gross_salary_month","base_salary","bonus_total","adjustment_total","working_days","vacation_days"]
    rows = []
    for row in summary_rows:
        bonus_total = row['bonus_total'] if include_bonuses else 0.0
        adjustment_total = row['adjustment_total']
        gross_salary = row['base_salary'] + bonus_total + adjustment_total
        rows.append([
            row['employee_id'], row['first_name'], row['last_name'], row['cnp'],
            f"{gross_salary:.2f}", f"{row['base_salary']:.2f}", f"{bonus_total:.2f}", f"{adjustment_total:.2f}", month_info.working_days, row['vacation_days']
        ])

    # Directory and file path
    dir_path = os.path.join(BASE_REPORT_DIR, 'csv', f"{year}-{month:02d}")
    ensure_dir(dir_path)
    file_path = os.path.join(dir_path, f"{manager_id}.csv")
    write_csv(file_path, headers, rows)

    # Load bytes for inline storage
    with open(file_path, 'rb') as f:
        content_bytes = f.read()
    report = repo_create_report_file(db, path=file_path, type='csv', owner_id=manager_id, archived=False, content=content_bytes)
    return report


def send_manager_csv(db: Session, manager_id: UUID, year: int, month: int, idempotency_key: str | None = None) -> dict:
    # Idempotency check
    if idempotency_key:
        key_obj = repo_get_idempotency_key_by_key(db, idempotency_key)
        endpoint_sig = f"send_manager_csv:{manager_id}:{year}-{month:02d}"
        if key_obj:
            # If same endpoint and succeeded, return cached reference
            if key_obj.endpoint == endpoint_sig and key_obj.status == 'succeeded':
                return {"status": "cached", "idempotent": True, "archivePath": key_obj.result_path}
            # If in progress, abort duplicate run
            if key_obj.endpoint == endpoint_sig and key_obj.status == 'started':
                raise HTTPException(status_code=409, detail="Operation already in progress")
        else:
            # Create started record
            repo_create_idempotency_key(db, key=idempotency_key, endpoint=endpoint_sig, status='started')

    report = generate_manager_csv(db, manager_id, year, month)
    manager = _get_manager(db, manager_id)
    send_email(manager.email, f"Monthly CSV {year}-{month:02d}", "Attached CSV report", [report.path])

    archive_dir = os.path.join(BASE_REPORT_DIR, 'archives', f"{year}-{month:02d}")
    ensure_dir(archive_dir)
    archive_path = os.path.join(archive_dir, os.path.basename(report.path))
    try:
        shutil.copy2(report.path, archive_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to archive CSV: {e}")
    report = repo_update_report_file(db, str(report.id), archived=True, path=archive_path)

    if idempotency_key:
        key_obj = repo_get_idempotency_key_by_key(db, idempotency_key)
        if key_obj:
            repo_mark_idempotency_key_succeeded(db, key_obj, result_path=archive_path)
    return {"status":"sent","fileId": str(report.id), "archived": True, "archivePath": archive_path, "idempotent": bool(idempotency_key)}


def generate_employee_pdfs(db: Session, manager_id: UUID, year: int, month: int, overwrite: bool=False) -> dict:
    manager = _get_manager(db, manager_id)
    subs = _get_subordinates(db, manager_id)
    month_info = _get_month_info(db, year, month)
    if not subs:
        return {"generated":0, "fileIds": []}
    summary_rows = _get_summary(db, manager_id, year, month)

    file_ids = []
    # Map summary by employee_id for quick lookup
    summary_map = {r['employee_id']: r for r in summary_rows}
    for e in subs:
        data = summary_map.get(str(e.id), None)
        if not data:
            bonus_total = 0.0
            adjustment_total = 0.0
            vacation_days = 0
            base_salary = float(e.base_salary)
        else:
            bonus_total = data['bonus_total']
            adjustment_total = data['adjustment_total']
            vacation_days = data['vacation_days']
            base_salary = data['base_salary']
        gross_salary = base_salary + bonus_total + adjustment_total
        dir_path = os.path.join(BASE_REPORT_DIR, 'pdf', f"{year}-{month:02d}")
        ensure_dir(dir_path)
        pdf_path = os.path.join(dir_path, f"{e.id}.pdf")
        if not overwrite and os.path.exists(pdf_path):
            # Already exists; inline its content if we create a record now
            with open(pdf_path, 'rb') as f:
                pdf_bytes = f.read()
            report = repo_create_report_file(db, path=pdf_path, type='pdf', owner_id=e.id, archived=False, content=pdf_bytes)
            file_ids.append(str(report.id))
            continue
        build_salary_pdf(pdf_path, {
            'year': year,
            'month': month,
            'employee_id': str(e.id),
            'name': f"{e.first_name} {e.last_name}",
            'cnp': e.cnp,
            'hire_date': e.hire_date,
            'manager_name': f"{manager.first_name} {manager.last_name}",
            'base_salary': f"{base_salary:.2f}",
            'bonus_total': f"{bonus_total:.2f}",
            'adjustment_total': f"{adjustment_total:.2f}",
            'gross_salary': f"{gross_salary:.2f}",
            'working_days': month_info.working_days,
            'vacation_days': vacation_days,
        })
        with open(pdf_path, 'rb') as f:
            pdf_bytes = f.read()
        report = repo_create_report_file(db, path=pdf_path, type='pdf', owner_id=e.id, archived=False, content=pdf_bytes)
        file_ids.append(str(report.id))
    return {"generated": len(file_ids), "fileIds": file_ids}


def send_employee_pdfs(db: Session, manager_id: UUID, year: int, month: int, regenerate_missing: bool=False, idempotency_key: str | None = None) -> dict:
    if idempotency_key:
        key_obj = repo_get_idempotency_key_by_key(db, idempotency_key)
        endpoint_sig = f"send_employee_pdfs:{manager_id}:{year}-{month:02d}"
        if key_obj:
            if key_obj.endpoint == endpoint_sig and key_obj.status == 'succeeded':
                return {"status": "cached", "idempotent": True, "archiveZipPath": key_obj.result_path}
            if key_obj.endpoint == endpoint_sig and key_obj.status == 'started':
                raise HTTPException(status_code=409, detail="Operation already in progress")
        else:
            repo_create_idempotency_key(db, key=idempotency_key, endpoint=endpoint_sig, status='started')

    gen = generate_employee_pdfs(db, manager_id, year, month, overwrite=regenerate_missing)
    manager = _get_manager(db, manager_id)
    subs = _get_subordinates(db, manager_id)
    sent = 0
    pdf_paths = []
    for e in subs:
        pdf_path = os.path.join(BASE_REPORT_DIR, 'pdf', f"{year}-{month:02d}", f"{e.id}.pdf")
        if os.path.exists(pdf_path):
            send_email(e.email, f"Salary Slip {year}-{month:02d}", "Attached PDF salary slip", [pdf_path])
            pdf_paths.append(pdf_path)
            sent += 1
    archive_root = os.path.join(BASE_REPORT_DIR, 'archives', f"{year}-{month:02d}")
    archive_pdfs_dir = os.path.join(archive_root, 'pdfs')
    ensure_dir(archive_pdfs_dir)
    archived_count = 0
    from db.repositories import repo_get_report_file_by_path, repo_update_report_file
    for p in pdf_paths:
        archive_path = os.path.join(archive_pdfs_dir, os.path.basename(p))
        try:
            shutil.copy2(p, archive_path)
            archived_count += 1
            report_rec = repo_get_report_file_by_path(db, p)
            if report_rec:
                repo_update_report_file(db, str(report_rec.id), archived=True, path=archive_path)
        except Exception:
            pass
    zip_path = os.path.join(archive_root, f"{manager_id}_pdfs.zip")
    zip_paths(pdf_paths, zip_path)
    with open(zip_path, 'rb') as f:
        zip_bytes = f.read()
    archive_report = repo_create_report_file(db, path=zip_path, type='zip', owner_id=manager_id, archived=True, content=zip_bytes)
    if idempotency_key:
        key_obj = repo_get_idempotency_key_by_key(db, idempotency_key)
        if key_obj:
            repo_mark_idempotency_key_succeeded(db, key_obj, result_path=zip_path)
    return {"sent": sent, "archivedPdfs": archived_count, "archiveZipId": str(archive_report.id), "archiveZipPath": zip_path, "idempotent": bool(idempotency_key)}
