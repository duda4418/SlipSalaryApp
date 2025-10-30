# models.py
import enum, uuid
from datetime import datetime, date
from sqlalchemy import (
    String, Date, Enum, ForeignKey, Numeric, UniqueConstraint,
    Boolean, DateTime, Integer
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column
from db.base import Base 

class SalaryComponentType(enum.Enum):
    BASE = "base"
    BONUS = "bonus"
    ADJUSTMENT = "adjustment"

class User(Base):
    __tablename__ = "users"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=True)  # demo can leave null
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    employee: Mapped["Employee"] = relationship(back_populates="user", uselist=False)

class Employee(Base):
    __tablename__ = "employees"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("users.id"), unique=True, nullable=True)
    first_name: Mapped[str] = mapped_column(String(255), nullable=False)
    last_name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    cnp: Mapped[str] = mapped_column(String(32), unique=True, nullable=False)
    hire_date: Mapped[date] = mapped_column(Date, nullable=False)
    base_salary: Mapped[float] = mapped_column(Numeric(12,2), nullable=False)

    manager_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("employees.id"), nullable=True)

    # relations
    user: Mapped["User | None"] = relationship(back_populates="employee")
    manager: Mapped["Employee | None"] = relationship(remote_side=[id], backref="subordinates")
    vacations: Mapped[list["Vacation"]] = relationship(back_populates="employee", cascade="all, delete-orphan")
    components: Mapped[list["SalaryComponent"]] = relationship(back_populates="employee", cascade="all, delete-orphan")

class SalaryComponent(Base):
    __tablename__ = "salary_components"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    employee_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("employees.id"), nullable=False, index=True)
    year: Mapped[int] = mapped_column(nullable=False)
    month: Mapped[int] = mapped_column(nullable=False)
    type: Mapped[SalaryComponentType] = mapped_column(Enum(SalaryComponentType), nullable=False)
    amount: Mapped[float] = mapped_column(Numeric(12,2), nullable=False)
    note: Mapped[str | None] = mapped_column(String(255), nullable=True)

    employee: Mapped["Employee"] = relationship(back_populates="components")
    __table_args__ = (UniqueConstraint("employee_id", "year", "month", "type", name="uq_salary_component"),)

class Vacation(Base):
    __tablename__ = "vacations"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    employee_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("employees.id"), index=True)
    year: Mapped[int] = mapped_column(nullable=False)
    month: Mapped[int] = mapped_column(nullable=False)
    days_taken: Mapped[int] = mapped_column(Integer, default=0)

    employee: Mapped["Employee"] = relationship(back_populates="vacations")
    __table_args__ = (UniqueConstraint("employee_id", "year", "month", name="uq_vacation"),)

class IdempotencyKey(Base):
    __tablename__ = "idempotency_keys"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    key: Mapped[str] = mapped_column(String(128), unique=True, index=True)
    endpoint: Mapped[str] = mapped_column(String(128))
    status: Mapped[str] = mapped_column(String(32), default="started") # started/succeeded/failed
    result_path: Mapped[str | None] = mapped_column(String(512), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class ReportFile(Base):
    __tablename__ = "report_files"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    path: Mapped[str] = mapped_column(String(512), nullable=False)
    type: Mapped[str] = mapped_column(String(32))  # csv or pdf
    owner_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True)) # manager_id or employee_id depending on use
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    archived: Mapped[bool] = mapped_column(Boolean, default=False)

class MonthInfo(Base):
    __tablename__ = "months"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    year: Mapped[int] = mapped_column(nullable=False)
    month: Mapped[int] = mapped_column(nullable=False)
    working_days: Mapped[int] = mapped_column(nullable=False)
    __table_args__ = (UniqueConstraint("year", "month", name="uq_monthinfo"),)
