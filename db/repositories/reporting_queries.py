from sqlalchemy.orm import Session
from fastapi import HTTPException
from sqlalchemy import func, case, literal_column, select
from db import models

__all__ = [
    'repo_get_manager',
    'repo_list_subordinates',
    'repo_list_salary_components_for_employees_month',
    'repo_list_vacations_for_employees_month',
    'repo_aggregate_employee_month_summary',
]

def repo_get_manager(db: Session, manager_id: str):
    mgr = db.get(models.Employee, manager_id)
    if not mgr:
        raise HTTPException(status_code=404, detail="Manager not found")
    return mgr

def repo_list_subordinates(db: Session, manager_id: str):
    return db.query(models.Employee).filter(models.Employee.manager_id == manager_id).all()

def repo_list_salary_components_for_employees_month(db: Session, employee_ids: list[str], year: int, month: int):
    if not employee_ids:
        return []
    return db.query(models.SalaryComponent).filter(
        models.SalaryComponent.employee_id.in_(employee_ids),
        models.SalaryComponent.year == year,
        models.SalaryComponent.month == month
    ).all()

def repo_list_vacations_for_employees_month(db: Session, employee_ids: list[str], year: int, month: int):
    if not employee_ids:
        return []
    return db.query(models.Vacation).filter(
        models.Vacation.employee_id.in_(employee_ids),
        models.Vacation.year == year,
        models.Vacation.month == month
    ).all()

def repo_aggregate_employee_month_summary(db: Session, manager_id: str, year: int, month: int):
    """Return list of dicts with per-employee aggregated financial data for a manager."""
    subq_emps = select(models.Employee.id).where(models.Employee.manager_id == manager_id).subquery()
    comp_aggr = select(
        models.SalaryComponent.employee_id.label('employee_id'),
        func.sum(case((models.SalaryComponent.type == models.SalaryComponentType.bonus, models.SalaryComponent.amount), else_=0)).label('bonus_total'),
        func.sum(case((models.SalaryComponent.type == models.SalaryComponentType.adjustment, models.SalaryComponent.amount), else_=0)).label('adjustment_total')
    ).where(
        models.SalaryComponent.employee_id.in_(select(subq_emps.c.id)),
        models.SalaryComponent.year == year,
        models.SalaryComponent.month == month
    ).group_by(models.SalaryComponent.employee_id).subquery()
    vac_aggr = select(
        models.Vacation.employee_id.label('employee_id'),
        func.sum(models.Vacation.days_taken).label('vacation_days')
    ).where(
        models.Vacation.employee_id.in_(select(subq_emps.c.id)),
        models.Vacation.year == year,
        models.Vacation.month == month
    ).group_by(models.Vacation.employee_id).subquery()
    query = db.query(
        models.Employee.id.label('employee_id'),
        models.Employee.first_name,
        models.Employee.last_name,
        models.Employee.cnp,
        models.Employee.base_salary,
        func.coalesce(comp_aggr.c.bonus_total, literal_column('0')).label('bonus_total'),
        func.coalesce(comp_aggr.c.adjustment_total, literal_column('0')).label('adjustment_total'),
        func.coalesce(vac_aggr.c.vacation_days, literal_column('0')).label('vacation_days')
    ).filter(models.Employee.id.in_(select(subq_emps.c.id)))
    query = query.outerjoin(comp_aggr, models.Employee.id == comp_aggr.c.employee_id).outerjoin(vac_aggr, models.Employee.id == vac_aggr.c.employee_id)
    results = []
    for row in query.all():
        results.append({
            'employee_id': str(row.employee_id),
            'first_name': row.first_name,
            'last_name': row.last_name,
            'cnp': row.cnp,
            'base_salary': float(row.base_salary),
            'bonus_total': float(row.bonus_total),
            'adjustment_total': float(row.adjustment_total),
            'vacation_days': int(row.vacation_days),
        })
    return results
