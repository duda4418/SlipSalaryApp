from core.config import CamelModel
from typing import Optional
from uuid import UUID
from datetime import date

class UserResponse(CamelModel):
	id: UUID
	email: str
	password_hash: Optional[str]
	is_active: bool
	created_at: date


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


class MonthInfoResponse(CamelModel):
	id: UUID
	year: int
	month: int
	working_days: int


class SalaryComponentResponse(CamelModel):
	id: UUID
	employee_id: UUID
	year: int
	month: int
	type: str
	amount: float
	note: Optional[str]


class VacationResponse(CamelModel):
	id: UUID
	employee_id: UUID
	year: int
	month: int
	days_taken: int


class IdempotencyKeyResponse(CamelModel):
	id: UUID
	key: str
	endpoint: str
	status: str
	result_path: Optional[str]
	created_at: date
	updated_at: date


class ReportFileResponse(CamelModel):
	id: UUID
	path: str
	type: str
	owner_id: UUID
	created_at: date
	archived: bool


