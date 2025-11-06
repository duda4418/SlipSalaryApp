"""Initial database schema.

Revision ID: 15b3a7b2f2d4
Revises: None
Create Date: 2025-11-06
"""
from __future__ import annotations

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "15b3a7b2f2d4"
down_revision = None
branch_labels = None
depends_on = None

# Enum for salary component types
SALARY_COMPONENT_ENUM_NAME = "salarycomponenttype"


def upgrade() -> None:


    # employees table
    op.create_table(
        "employees",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("email", sa.String(255), nullable=False),
        sa.Column("password_hash", sa.String(255), nullable=True),
        sa.Column("is_active", sa.Boolean, nullable=False, server_default=sa.text("true")),
        sa.Column("is_manager", sa.Boolean, nullable=False, server_default=sa.text("false")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("first_name", sa.String(255), nullable=False),
        sa.Column("last_name", sa.String(255), nullable=False),
        sa.Column("cnp", sa.String(32), nullable=False),
        sa.Column("hire_date", sa.Date, nullable=False),
        sa.Column("base_salary", sa.Numeric(12, 2), nullable=False),
        sa.Column("manager_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.ForeignKeyConstraint(["manager_id"], ["employees.id"], name="fk_employees_manager_id_employees"),
        sa.UniqueConstraint("email", name="uq_employees_email"),
        sa.UniqueConstraint("cnp", name="uq_employees_cnp"),
    )
    op.create_index("ix_employees_email", "employees", ["email"], unique=False)

    # months table (MonthInfo)
    op.create_table(
        "months",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("year", sa.Integer, nullable=False),
        sa.Column("month", sa.Integer, nullable=False),
        sa.Column("working_days", sa.Integer, nullable=False),
        sa.UniqueConstraint("year", "month", name="uq_monthinfo"),
    )

    # salary_components table
    op.create_table(
        "salary_components",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("employee_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("year", sa.Integer, nullable=False),
        sa.Column("month", sa.Integer, nullable=False),
        sa.Column("type", sa.Enum("base", "bonus", "adjustment", name=SALARY_COMPONENT_ENUM_NAME), nullable=False),
        sa.Column("amount", sa.Numeric(12, 2), nullable=False),
        sa.Column("note", sa.String(255), nullable=True),
        sa.ForeignKeyConstraint(["employee_id"], ["employees.id"], name="fk_salary_components_employee_id_employees"),
        sa.UniqueConstraint("employee_id", "year", "month", "type", name="uq_salary_component"),
    )
    op.create_index("ix_salary_components_employee_id", "salary_components", ["employee_id"], unique=False)

    # vacations table
    op.create_table(
        "vacations",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("employee_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("year", sa.Integer, nullable=False),
        sa.Column("month", sa.Integer, nullable=False),
        sa.Column("days_taken", sa.Integer, nullable=False, server_default="0"),
        sa.ForeignKeyConstraint(["employee_id"], ["employees.id"], name="fk_vacations_employee_id_employees"),
        sa.UniqueConstraint("employee_id", "year", "month", name="uq_vacation"),
    )
    op.create_index("ix_vacations_employee_id", "vacations", ["employee_id"], unique=False)

    # idempotency_keys table
    op.create_table(
        "idempotency_keys",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("key", sa.String(128), nullable=False),
        sa.Column("endpoint", sa.String(128), nullable=False),
        sa.Column("status", sa.String(32), nullable=False, server_default="started"),
        sa.Column("result_path", sa.String(512), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("key", name="uq_idempotency_keys_key"),
    )
    op.create_index("ix_idempotency_keys_key", "idempotency_keys", ["key"], unique=False)

    # report_files table
    op.create_table(
        "report_files",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("path", sa.String(512), nullable=False),
        sa.Column("type", sa.String(32), nullable=False),
        sa.Column("owner_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("archived", sa.Boolean, nullable=False, server_default=sa.text("false")),
        sa.Column("content", sa.LargeBinary, nullable=True),
        sa.Column("content_type", sa.String(64), nullable=True),
        sa.Column("size_bytes", sa.Integer, nullable=True),
    )

    # refresh_tokens table
    op.create_table(
        "refresh_tokens",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("employee_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("token_hash", sa.String(255), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("revoked", sa.Boolean, nullable=False, server_default=sa.text("false")),
        sa.Column("replaced_by", postgresql.UUID(as_uuid=True), nullable=True),
        sa.ForeignKeyConstraint(["employee_id"], ["employees.id"], name="fk_refresh_tokens_employee_id_employees"),
        sa.ForeignKeyConstraint(["replaced_by"], ["refresh_tokens.id"], name="fk_refresh_tokens_replaced_by_refresh_tokens"),
        sa.UniqueConstraint("token_hash", name="uq_refresh_tokens_token_hash"),
    )
    op.create_index("ix_refresh_tokens_employee_id", "refresh_tokens", ["employee_id"], unique=False)


def downgrade() -> None:
    # Drop tables in reverse order to satisfy FKs
    op.drop_index("ix_refresh_tokens_employee_id", table_name="refresh_tokens")
    op.drop_table("refresh_tokens")

    op.drop_table("report_files")

    op.drop_index("ix_idempotency_keys_key", table_name="idempotency_keys")
    op.drop_table("idempotency_keys")

    op.drop_index("ix_vacations_employee_id", table_name="vacations")
    op.drop_table("vacations")

    op.drop_index("ix_salary_components_employee_id", table_name="salary_components")
    op.drop_table("salary_components")

    op.drop_table("months")

    op.drop_index("ix_employees_email", table_name="employees")
    op.drop_table("employees")

    # Finally drop enum type
    op.execute(f'DROP TYPE IF EXISTS {SALARY_COMPONENT_ENUM_NAME}')
