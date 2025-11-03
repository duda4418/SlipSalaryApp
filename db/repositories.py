from sqlalchemy.orm import Session
from db import models
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException

# (User model removed - merged into Employee)

# Employee repositories
def repo_list_employees(db: Session):
	return db.query(models.Employee).all()

def repo_get_employee_by_id(db: Session, employee_id: str):
	employee = db.get(models.Employee, employee_id)
	if not employee:
		raise HTTPException(status_code=404, detail="Employee not found")
	return employee

def repo_create_employee(db: Session, **data):
	employee = models.Employee(**data)
	db.add(employee)
	try:
		db.commit()
	except IntegrityError as e:
		db.rollback()
		raise HTTPException(status_code=400, detail="Employee violates unique constraint") from e
	db.refresh(employee)
	return employee

def repo_update_employee(db: Session, employee_id: str, **data):
	employee = db.get(models.Employee, employee_id)
	if not employee:
		raise HTTPException(status_code=404, detail="Employee not found")
	for key, value in data.items():
		setattr(employee, key, value)
	try:
		db.commit()
	except IntegrityError as e:
		db.rollback()
		raise HTTPException(status_code=400, detail="Employee violates unique constraint") from e
	db.refresh(employee)
	return employee

def repo_delete_employee(db: Session, employee_id: str):
	employee = db.get(models.Employee, employee_id)
	if not employee:
		raise HTTPException(status_code=404, detail="Employee not found")
	db.delete(employee)
	db.commit()
	return {"deleted": True, "id": employee_id}

############################
# NOTE: User mutations removed
############################

############################
# SalaryComponent mutations
############################
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

############################
# Vacation mutations
############################
def repo_create_vacation(db: Session, **data):
	vacation = models.Vacation(**data)
	db.add(vacation)
	try:
		db.commit()
	except IntegrityError as e:
		db.rollback()
		raise HTTPException(status_code=400, detail="Vacation violates unique constraint") from e
	db.refresh(vacation)
	return vacation

def repo_update_vacation(db: Session, vacation_id: str, **data):
	vacation = db.get(models.Vacation, vacation_id)
	if not vacation:
		raise HTTPException(status_code=404, detail="Vacation not found")
	for k, v in data.items():
		setattr(vacation, k, v)
	try:
		db.commit()
	except IntegrityError as e:
		db.rollback()
		raise HTTPException(status_code=400, detail="Vacation violates unique constraint") from e
	db.refresh(vacation)
	return vacation

def repo_delete_vacation(db: Session, vacation_id: str):
	vacation = db.get(models.Vacation, vacation_id)
	if not vacation:
		raise HTTPException(status_code=404, detail="Vacation not found")
	db.delete(vacation)
	db.commit()
	return {"deleted": True, "id": vacation_id}

############################
# MonthInfo mutations
############################
def repo_create_month(db: Session, **data):
	month = models.MonthInfo(**data)
	db.add(month)
	try:
		db.commit()
	except IntegrityError as e:
		db.rollback()
		raise HTTPException(status_code=400, detail="Month violates unique constraint") from e
	db.refresh(month)
	return month

def repo_update_month(db: Session, month_id: str, **data):
	month = db.get(models.MonthInfo, month_id)
	if not month:
		raise HTTPException(status_code=404, detail="Month not found")
	for k, v in data.items():
		setattr(month, k, v)
	try:
		db.commit()
	except IntegrityError as e:
		db.rollback()
		raise HTTPException(status_code=400, detail="Month violates unique constraint") from e
	db.refresh(month)
	return month

def repo_delete_month(db: Session, month_id: str):
	month = db.get(models.MonthInfo, month_id)
	if not month:
		raise HTTPException(status_code=404, detail="Month not found")
	db.delete(month)
	db.commit()
	return {"deleted": True, "id": month_id}

############################
# IdempotencyKey mutations
############################
def repo_create_idempotency_key(db: Session, **data):
	key = models.IdempotencyKey(**data)
	db.add(key)
	try:
		db.commit()
	except IntegrityError as e:
		db.rollback()
		raise HTTPException(status_code=400, detail="Idempotency key violates unique constraint") from e
	db.refresh(key)
	return key

def repo_update_idempotency_key(db: Session, key_id: str, **data):
	key = db.get(models.IdempotencyKey, key_id)
	if not key:
		raise HTTPException(status_code=404, detail="Idempotency key not found")
	for k, v in data.items():
		setattr(key, k, v)
	try:
		db.commit()
	except IntegrityError as e:
		db.rollback()
		raise HTTPException(status_code=400, detail="Idempotency key violates unique constraint") from e
	db.refresh(key)
	return key

def repo_delete_idempotency_key(db: Session, key_id: str):
	key = db.get(models.IdempotencyKey, key_id)
	if not key:
		raise HTTPException(status_code=404, detail="Idempotency key not found")
	db.delete(key)
	db.commit()
	return {"deleted": True, "id": key_id}

############################
# ReportFile mutations
############################
def repo_create_report_file(db: Session, **data):
	report = models.ReportFile(**data)
	db.add(report)
	try:
		db.commit()
	except IntegrityError as e:
		db.rollback()
		raise HTTPException(status_code=400, detail="Report file violates unique constraint") from e
	db.refresh(report)
	return report

def repo_update_report_file(db: Session, report_id: str, **data):
	report = db.get(models.ReportFile, report_id)
	if not report:
		raise HTTPException(status_code=404, detail="Report not found")
	for k, v in data.items():
		setattr(report, k, v)
	try:
		db.commit()
	except IntegrityError as e:
		db.rollback()
		raise HTTPException(status_code=400, detail="Report file violates unique constraint") from e
	db.refresh(report)
	return report

def repo_delete_report_file(db: Session, report_id: str):
	report = db.get(models.ReportFile, report_id)
	if not report:
		raise HTTPException(status_code=404, detail="Report not found")
	db.delete(report)
	db.commit()
	return {"deleted": True, "id": report_id}

# SalaryComponent repositories
def repo_list_salary_components(db: Session):
	return db.query(models.SalaryComponent).all()

def repo_get_salary_component_by_id(db: Session, component_id: str):
	component = db.get(models.SalaryComponent, component_id)
	if not component:
		raise HTTPException(status_code=404, detail="Salary component not found")
	return component

# Vacation repositories
def repo_list_vacations(db: Session):
	return db.query(models.Vacation).all()

def repo_get_vacation_by_id(db: Session, vacation_id: str):
	vacation = db.get(models.Vacation, vacation_id)
	if not vacation:
		raise HTTPException(status_code=404, detail="Vacation not found")
	return vacation

# MonthInfo repositories
def repo_list_months(db: Session):
	return db.query(models.MonthInfo).all()

def repo_get_month_by_id(db: Session, month_id: str):
	month = db.get(models.MonthInfo, month_id)
	if not month:
		raise HTTPException(status_code=404, detail="Month not found")
	return month

# IdempotencyKey repositories
def repo_list_idempotency_keys(db: Session):
	return db.query(models.IdempotencyKey).all()

def repo_get_idempotency_key_by_id(db: Session, key_id: str):
	key = db.get(models.IdempotencyKey, key_id)
	if not key:
		raise HTTPException(status_code=404, detail="Idempotency key not found")
	return key

# ReportFile repositories
def repo_list_report_files(db: Session):
	return db.query(models.ReportFile).all()

def repo_get_report_file_by_id(db: Session, report_id: str):
	report = db.get(models.ReportFile, report_id)
	if not report:
		raise HTTPException(status_code=404, detail="Report not found")
	return report

############################
# Reporting helper queries
############################
def repo_get_manager(db: Session, manager_id: str):
	mgr = db.get(models.Employee, manager_id)
	if not mgr:
		raise HTTPException(status_code=404, detail="Manager not found")
	return mgr

def repo_list_subordinates(db: Session, manager_id: str):
	return db.query(models.Employee).filter(models.Employee.manager_id == manager_id).all()

def repo_get_month_info_by_year_month(db: Session, year: int, month: int):
	mi = db.query(models.MonthInfo).filter(models.MonthInfo.year == year, models.MonthInfo.month == month).first()
	if not mi:
		raise HTTPException(status_code=400, detail="Month info not defined")
	return mi

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
	"""Return list of dicts with per-employee aggregated financial data for a manager.
	Fields: employee_id, first_name, last_name, cnp, base_salary, bonus_total, adjustment_total, vacation_days
	"""
	from sqlalchemy import func, case, literal_column
	# Subordinates of manager
	subq_emps = db.query(models.Employee.id).filter(models.Employee.manager_id == manager_id).subquery()
	# Components aggregation
	comp_aggr = db.query(
		models.SalaryComponent.employee_id.label('employee_id'),
		func.sum(case((models.SalaryComponent.type == models.SalaryComponentType.bonus, models.SalaryComponent.amount), else_=0)).label('bonus_total'),
		func.sum(case((models.SalaryComponent.type == models.SalaryComponentType.adjustment, models.SalaryComponent.amount), else_=0)).label('adjustment_total')
	).filter(
		models.SalaryComponent.employee_id.in_(subq_emps),
		models.SalaryComponent.year == year,
		models.SalaryComponent.month == month
	).group_by(models.SalaryComponent.employee_id).subquery()
	# Vacation aggregation
	vac_aggr = db.query(
		models.Vacation.employee_id.label('employee_id'),
		func.sum(models.Vacation.days_taken).label('vacation_days')
	).filter(
		models.Vacation.employee_id.in_(subq_emps),
		models.Vacation.year == year,
		models.Vacation.month == month
	).group_by(models.Vacation.employee_id).subquery()
	# Join employees with aggregates
	query = db.query(
		models.Employee.id.label('employee_id'),
		models.Employee.first_name,
		models.Employee.last_name,
		models.Employee.cnp,
		models.Employee.base_salary,
		func.coalesce(comp_aggr.c.bonus_total, literal_column('0')).label('bonus_total'),
		func.coalesce(comp_aggr.c.adjustment_total, literal_column('0')).label('adjustment_total'),
		func.coalesce(vac_aggr.c.vacation_days, literal_column('0')).label('vacation_days')
	).filter(models.Employee.id.in_(subq_emps))
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

