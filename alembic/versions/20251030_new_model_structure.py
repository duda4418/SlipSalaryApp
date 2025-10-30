"""
Initial migration for new models: removes managers table, updates employees for self-referential manager_id, unique cnp, nullable user_id, and updates all relationships.
"""
from alembic import op
import sqlalchemy as sa
import uuid

revision = '20251030_new_model_structure'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():

    # ### Create users table ###
    op.create_table(
        'users',
        sa.Column('id', sa.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column('email', sa.String(255), unique=True, index=True, nullable=False),
        sa.Column('password_hash', sa.String(255), nullable=True),
        sa.Column('is_active', sa.Boolean(), default=True),
        sa.Column('created_at', sa.DateTime(), default=sa.func.now()),
    )

    # ### Create employees table ###
    op.create_table(
        'employees',
        sa.Column('id', sa.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column('user_id', sa.UUID(as_uuid=True), sa.ForeignKey('users.id'), unique=True, nullable=True),
        sa.Column('first_name', sa.String(255), nullable=False),
        sa.Column('last_name', sa.String(255), nullable=False),
        sa.Column('email', sa.String(255), unique=True, index=True, nullable=False),
        sa.Column('cnp', sa.String(32), unique=True, nullable=False),
        sa.Column('hire_date', sa.Date(), nullable=False),
        sa.Column('base_salary', sa.Numeric(12,2), nullable=False),
        sa.Column('manager_id', sa.UUID(as_uuid=True), sa.ForeignKey('employees.id'), nullable=True),
    )

    # ### Create salary_components table ###
    op.create_table(
        'salary_components',
        sa.Column('id', sa.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column('employee_id', sa.UUID(as_uuid=True), sa.ForeignKey('employees.id'), nullable=False, index=True),
        sa.Column('year', sa.Integer(), nullable=False),
        sa.Column('month', sa.Integer(), nullable=False),
        sa.Column('type', sa.Enum('base', 'bonus', 'adjustment', name='salarycomponenttype'), nullable=False),
        sa.Column('amount', sa.Numeric(12,2), nullable=False),
        sa.Column('note', sa.String(255), nullable=True),
        sa.UniqueConstraint('employee_id', 'year', 'month', 'type', name='uq_salary_component'),
    )

    # ### Create vacations table ###
    op.create_table(
        'vacations',
        sa.Column('id', sa.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column('employee_id', sa.UUID(as_uuid=True), sa.ForeignKey('employees.id'), index=True),
        sa.Column('year', sa.Integer(), nullable=False),
        sa.Column('month', sa.Integer(), nullable=False),
        sa.Column('days_taken', sa.Integer(), default=0),
        sa.UniqueConstraint('employee_id', 'year', 'month', name='uq_vacation'),
    )

    # ### Create idempotency_keys table ###
    op.create_table(
        'idempotency_keys',
        sa.Column('id', sa.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column('key', sa.String(128), unique=True, index=True),
        sa.Column('endpoint', sa.String(128)),
        sa.Column('status', sa.String(32), default='started'),
        sa.Column('result_path', sa.String(512), nullable=True),
        sa.Column('created_at', sa.DateTime(), default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), default=sa.func.now()),
    )

    # ### Create report_files table ###
    op.create_table(
        'report_files',
        sa.Column('id', sa.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column('path', sa.String(512), nullable=False),
        sa.Column('type', sa.String(32)),
        sa.Column('owner_id', sa.UUID(as_uuid=True)),
        sa.Column('created_at', sa.DateTime(), default=sa.func.now()),
        sa.Column('archived', sa.Boolean(), default=False),
    )

    # ### Create months table ###
    op.create_table(
        'months',
        sa.Column('id', sa.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column('year', sa.Integer(), nullable=False),
        sa.Column('month', sa.Integer(), nullable=False),
        sa.Column('working_days', sa.Integer(), nullable=False),
        sa.UniqueConstraint('year', 'month', name='uq_monthinfo'),
    )

def downgrade():
    op.drop_table('months')
    op.drop_table('report_files')
    op.drop_table('idempotency_keys')
    op.drop_table('vacations')
    op.drop_table('salary_components')
    op.drop_table('employees')
    op.drop_table('users')
    # managers table is not recreated
