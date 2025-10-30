"""Initial schema with deterministic constraint naming

Revision ID: 20251030_init_schema
Revises: 
Create Date: 2025-10-30

"""
from alembic import op
import sqlalchemy as sa

revision = '20251030_init_schema'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('email', sa.String(length=255), unique=True, index=True, nullable=False),
        sa.Column('first_name', sa.String(length=255), nullable=False),
        sa.Column('last_name', sa.String(length=255), nullable=False),
        sa.Column('cnp', sa.String(length=32), nullable=True),
        sa.Column('role', sa.Enum('MANAGER', 'EMPLOYEE', name='role'), nullable=False),
    )
    op.create_table(
        'managers',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.Integer(), unique=True, nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='fk_managers_user_id_users'),
    )
    op.create_table(
        'employees',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.Integer(), unique=True, nullable=False),
        sa.Column('manager_id', sa.Integer(), nullable=False),
        sa.Column('hire_date', sa.Date(), nullable=False),
        sa.Column('base_salary', sa.Numeric(12,2), nullable=False),
        sa.ForeignKeyConstraint(['manager_id'], ['managers.id'], name='fk_employees_manager_id_managers'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='fk_employees_user_id_users'),
    )
    op.create_table(
        'salary_components',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('employee_id', sa.Integer(), nullable=False),
        sa.Column('year', sa.Integer(), nullable=False),
        sa.Column('month', sa.Integer(), nullable=False),
        sa.Column('type', sa.Enum('BASE', 'BONUS', 'ADJUSTMENT', name='salarycomponenttype'), nullable=False),
        sa.Column('amount', sa.Numeric(12,2), nullable=False),
        sa.Column('note', sa.String(length=255), nullable=True),
        sa.ForeignKeyConstraint(['employee_id'], ['employees.id'], name='fk_salary_components_employee_id_employees'),
        sa.UniqueConstraint('employee_id', 'year', 'month', 'type', name='uq_salary_component'),
    )
    op.create_table(
        'vacations',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('employee_id', sa.Integer(), nullable=False),
        sa.Column('year', sa.Integer(), nullable=False),
        sa.Column('month', sa.Integer(), nullable=False),
        sa.Column('days_taken', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['employee_id'], ['employees.id'], name='fk_vacations_employee_id_employees'),
        sa.UniqueConstraint('employee_id', 'year', 'month', name='uq_vacation'),
    )
    op.create_table(
        'months',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('year', sa.Integer(), nullable=False),
        sa.Column('month', sa.Integer(), nullable=False),
        sa.Column('working_days', sa.Integer(), nullable=False),
        sa.UniqueConstraint('year', 'month', name='uq_monthinfo'),
    )
    op.create_table(
        'idempotency_keys',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('key', sa.String(length=128), unique=True, index=True, nullable=False),
        sa.Column('endpoint', sa.String(length=128), nullable=False),
        sa.Column('status', sa.String(length=32), nullable=False),
        sa.Column('result_path', sa.String(length=512), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )
    op.create_table(
        'report_files',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('path', sa.String(length=512), nullable=False),
        sa.Column('type', sa.String(length=32), nullable=False),
        sa.Column('owner_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('archived', sa.Boolean(), nullable=False),
    )

def downgrade():
    op.drop_table('report_files')
    op.drop_table('idempotency_keys')
    op.drop_table('months')
    op.drop_table('vacations')
    op.drop_table('salary_components')
    op.drop_table('employees')
    op.drop_table('managers')
    op.drop_table('users')
