from sqlalchemy import (
    Column, String, Date, Enum, ForeignKey, Numeric, UniqueConstraint,
    Boolean, DateTime, Integer
)
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime, date
from db.base import Base
import enum

class Role(enum.Enum):
    MANAGER = "manager"
    EMPLOYEE = "employee"

class SalaryComponentType(enum.Enum):
    BASE = "base"
    BONUS = "bonus"
    ADJUSTMENT = "adjustment"

class User(Base):
    __tablename__ = "users"
    id: Mapped[str] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    first_name: Mapped[str] = mapped_column(String(255), nullable=False)
    last_name: Mapped[str] = mapped_column(String(255), nullable=False)
    cnp: Mapped[str] = mapped_column(String(32), nullable=True)  # for employees
    role: Mapped[Role] = mapped_column(Enum(Role), nullable=False)

    employee = relationship("Employee", back_populates="user", uselist=False)
    manager = relationship("Manager", back_populates="user", uselist=False)

class Manager(Base):
    __tablename__ = "managers"
    id: Mapped[str] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), unique=True, nullable=False)

    user = relationship("User", back_populates="manager")
    employees = relationship("Employee", back_populates="manager")

class Employee(Base):
    __tablename__ = "employees"
    id: Mapped[str] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), unique=True, nullable=False)
    manager_id: Mapped[str] = mapped_column(ForeignKey("managers.id"), nullable=False)
    hire_date: Mapped[date] = mapped_column(Date, nullable=False)
    base_salary: Mapped[float] = mapped_column(Numeric(12,2), nullable=False)

    user = relationship("User", back_populates="employee")
    manager = relationship("Manager", back_populates="employees")
    vacations = relationship("Vacation", back_populates="employee")
    components = relationship("SalaryComponent", back_populates="employee")


class SalaryComponent(Base):
    __tablename__ = "salary_components"
    id: Mapped[str] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    employee_id: Mapped[str] = mapped_column(ForeignKey("employees.id"), nullable=False)
    year: Mapped[int] = mapped_column(nullable=False)
    month: Mapped[int] = mapped_column(nullable=False)
    type: Mapped[SalaryComponentType] = mapped_column(Enum(SalaryComponentType), nullable=False)
    amount: Mapped[float] = mapped_column(Numeric(12,2), nullable=False)
    note: Mapped[str] = mapped_column(String(255), nullable=True)

    employee = relationship("Employee", back_populates="components")
    __table_args__ = (UniqueConstraint("employee_id", "year", "month", "type", name="uq_salary_component"),)


class Vacation(Base):
    __tablename__ = "vacations"
    id: Mapped[str] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    employee_id: Mapped[str] = mapped_column(ForeignKey("employees.id"))
    year: Mapped[int] = mapped_column(nullable=False)
    month: Mapped[int] = mapped_column(nullable=False)
    days_taken: Mapped[int] = mapped_column(Integer, default=0)

    employee = relationship("Employee", back_populates="vacations")
    __table_args__ = (UniqueConstraint("employee_id", "year", "month", name="uq_vacation"),)

class IdempotencyKey(Base):
    __tablename__ = "idempotency_keys"
    id: Mapped[str] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    key: Mapped[str] = mapped_column(String(128), unique=True, index=True)
    endpoint: Mapped[str] = mapped_column(String(128))
    status: Mapped[str] = mapped_column(String(32), default="started") # started/succeeded/failed
    result_path: Mapped[str] = mapped_column(String(512), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class ReportFile(Base):
    __tablename__ = "report_files"
    id: Mapped[str] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    path: Mapped[str] = mapped_column(String(512), nullable=False)
    type: Mapped[str] = mapped_column(String(32))  # csv or pdf
    owner_id: Mapped[str] = mapped_column(UUID(as_uuid=True)) # manager_id or employee_id depending on use
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    archived: Mapped[bool] = mapped_column(Boolean, default=False)

class MonthInfo(Base):
    __tablename__ = "months"
    id: Mapped[str] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    year: Mapped[int] = mapped_column(nullable=False)
    month: Mapped[int] = mapped_column(nullable=False)
    working_days: Mapped[int] = mapped_column(nullable=False)
    __table_args__ = (UniqueConstraint("year", "month", name="uq_monthinfo"),)
