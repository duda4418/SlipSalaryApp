import os
from typing import List, Tuple
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
)
from utils.files import write_csv, zip_paths, ensure_dir
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

    report = repo_create_report_file(db, path=file_path, type='csv', owner_id=manager_id, archived=False)
    return report


def send_manager_csv(db: Session, manager_id: UUID, year: int, month: int) -> dict:
    report = generate_manager_csv(db, manager_id, year, month)
    manager = _get_manager(db, manager_id)
    send_email(manager.email, f"Monthly CSV {year}-{month:02d}", "Attached CSV report", [report.path])

    # Move/copy CSV into archive folder and mark archived
    archive_dir = os.path.join(BASE_REPORT_DIR, 'archives', f"{year}-{month:02d}")
    ensure_dir(archive_dir)
    archive_path = os.path.join(archive_dir, os.path.basename(report.path))
    try:
        import shutil
        shutil.copy2(report.path, archive_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to archive CSV: {e}")
    report = repo_update_report_file(db, str(report.id), archived=True, path=archive_path)
    return {"status":"sent","fileId": str(report.id), "archived": True, "archivePath": archive_path}


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
            # Already exists; optionally create ReportFile if missing
            report = repo_create_report_file(db, path=pdf_path, type='pdf', owner_id=e.id, archived=False)
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
        report = repo_create_report_file(db, path=pdf_path, type='pdf', owner_id=e.id, archived=False)
        file_ids.append(str(report.id))
    return {"generated": len(file_ids), "fileIds": file_ids}


def send_employee_pdfs(db: Session, manager_id: UUID, year: int, month: int, regenerate_missing: bool=False) -> dict:
    # For simplicity regenerate first
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
    # Archive individual PDFs then also create a zip bundle
    archive_root = os.path.join(BASE_REPORT_DIR, 'archives', f"{year}-{month:02d}")
    archive_pdfs_dir = os.path.join(archive_root, 'pdfs')
    ensure_dir(archive_pdfs_dir)
    import shutil
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
            # Skip failures but continue archiving others
            pass
    # Create zip of all archived PDFs for convenience/audit packaging
    zip_path = os.path.join(archive_root, f"{manager_id}_pdfs.zip")
    zip_paths(pdf_paths, zip_path)
    archive_report = repo_create_report_file(db, path=zip_path, type='zip', owner_id=manager_id, archived=True)
    return {"sent": sent, "archivedPdfs": archived_count, "archiveZipId": str(archive_report.id), "archiveZipPath": zip_path}
