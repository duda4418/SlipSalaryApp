from core.config import CamelModel
from typing import Optional
from uuid import UUID
from datetime import datetime, date


class UserResponse(CamelModel):
	id: UUID
	email: str
	password_hash: Optional[str]
	is_active: bool
	created_at: datetime

class UserCreate(CamelModel):
	email: str
	password_hash: Optional[str] = None
	is_active: Optional[bool] = True

class UserUpdate(CamelModel):
	email: Optional[str] = None
	password_hash: Optional[str] = None
	is_active: Optional[bool] = None


class EmployeeResponse(CamelModel):
	id: UUID
	user_id: Optional[UUID]
	first_name: str
	last_name: str
	email: str
	cnp: str
	hire_date: date
	base_salary: float
	manager_id: Optional[UUID]

class EmployeeCreate(CamelModel):
	user_id: Optional[UUID] = None
	first_name: str
	last_name: str
	email: str
	cnp: str
	hire_date: date
	base_salary: float
	manager_id: Optional[UUID] = None

class EmployeeUpdate(CamelModel):
	first_name: Optional[str] = None
	last_name: Optional[str] = None
	email: Optional[str] = None
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
	created_at: date
	updated_at: date

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
	created_at: date
	archived: bool

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


