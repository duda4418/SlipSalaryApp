from core.config import CamelModel
from typing import Optional
from uuid import UUID
from datetime import datetime, date


class EmployeeResponse(CamelModel):
	id: UUID
	email: str
	is_active: bool
	is_manager: bool
	created_at: datetime
	first_name: str
	last_name: str
	cnp: str
	hire_date: date
	base_salary: float
	manager_id: Optional[UUID]

class EmployeeCreate(CamelModel):
	email: str
	password_hash: Optional[str] = None
	is_active: Optional[bool] = True
	is_manager: Optional[bool] = False
	first_name: str
	last_name: str
	cnp: str
	hire_date: date
	base_salary: float
	manager_id: Optional[UUID] = None

class EmployeeUpdate(CamelModel):
	email: Optional[str] = None
	password_hash: Optional[str] = None
	is_active: Optional[bool] = None
	is_manager: Optional[bool] = None
	first_name: Optional[str] = None
	last_name: Optional[str] = None
	cnp: Optional[str] = None
	hire_date: Optional[date] = None
	base_salary: Optional[float] = None
	manager_id: Optional[UUID] = None


class MonthInfoResponse(CamelModel):
	id: UUID
	year: int
	month: int
	working_days: int

class MonthInfoCreate(CamelModel):
	year: int
	month: int
	working_days: int

class MonthInfoUpdate(CamelModel):
	year: Optional[int] = None
	month: Optional[int] = None
	working_days: Optional[int] = None


class SalaryComponentResponse(CamelModel):
	id: UUID
	employee_id: UUID
	year: int
	month: int
	type: str
	amount: float
	note: Optional[str]

class SalaryComponentCreate(CamelModel):
	employee_id: UUID
	year: int
	month: int
	type: str
	amount: float
	note: Optional[str] = None

class SalaryComponentUpdate(CamelModel):
	year: Optional[int] = None
	month: Optional[int] = None
	type: Optional[str] = None
	amount: Optional[float] = None
	note: Optional[str] = None


class VacationResponse(CamelModel):
	id: UUID
	employee_id: UUID
	year: int
	month: int
	days_taken: int

class VacationCreate(CamelModel):
	employee_id: UUID
	year: int
	month: int
	days_taken: int

class VacationUpdate(CamelModel):
	year: Optional[int] = None
	month: Optional[int] = None
	days_taken: Optional[int] = None


class IdempotencyKeyResponse(CamelModel):
	id: UUID
	key: str
	endpoint: str
	status: str
	result_path: Optional[str]
	created_at: datetime
	updated_at: datetime

class IdempotencyKeyCreate(CamelModel):
	key: str
	endpoint: str
	status: Optional[str] = "started"
	result_path: Optional[str] = None

class IdempotencyKeyUpdate(CamelModel):
	status: Optional[str] = None
	result_path: Optional[str] = None


class ReportFileResponse(CamelModel):
	id: UUID
	path: str
	type: str
	owner_id: UUID
	created_at: datetime
	archived: bool
	content_type: Optional[str]
	size_bytes: Optional[int]

class ReportFileCreate(CamelModel):
	path: str
	type: str
	owner_id: UUID
	archived: Optional[bool] = False

class ReportFileUpdate(CamelModel):
	path: Optional[str] = None
	type: Optional[str] = None
	owner_id: Optional[UUID] = None
	archived: Optional[bool] = None


