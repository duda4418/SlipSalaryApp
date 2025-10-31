from sqlalchemy.orm import Session
from db import models
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException

# User repositories
def repo_list_users(db: Session):
	return db.query(models.User).all()

def repo_get_user_by_id(db: Session, user_id: str):
	user = db.get(models.User, user_id)
	if not user:
		raise HTTPException(status_code=404, detail="User not found")
	return user

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
# User mutations
############################
def repo_create_user(db: Session, **data):
	user = models.User(**data)
	db.add(user)
	try:
		db.commit()
	except IntegrityError as e:
		db.rollback()
		raise HTTPException(status_code=400, detail="User violates unique constraint") from e
	db.refresh(user)
	return user

def repo_update_user(db: Session, user_id: str, **data):
	user = db.get(models.User, user_id)
	if not user:
		raise HTTPException(status_code=404, detail="User not found")
	for k, v in data.items():
		setattr(user, k, v)
	try:
		db.commit()
	except IntegrityError as e:
		db.rollback()
		raise HTTPException(status_code=400, detail="User violates unique constraint") from e
	db.refresh(user)
	return user

def repo_delete_user(db: Session, user_id: str):
	user = db.get(models.User, user_id)
	if not user:
		raise HTTPException(status_code=404, detail="User not found")
	db.delete(user)
	db.commit()
	return {"deleted": True, "id": user_id}

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

