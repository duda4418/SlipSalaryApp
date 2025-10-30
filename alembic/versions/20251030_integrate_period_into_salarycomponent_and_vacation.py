"""Integrate period into SalaryComponent and Vacation, remove PayrollPeriod

Revision ID: 20251030_integrate_period
Revises: f02e9defe838
Create Date: 2025-10-30

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '20251030_integrate_period'
down_revision = 'f02e9defe838'
branch_labels = None
depends_on = None

def upgrade():
    # Add year and month columns to salary_components
    op.add_column('salary_components', sa.Column('year', sa.Integer(), nullable=False, server_default='2025'))
    op.add_column('salary_components', sa.Column('month', sa.Integer(), nullable=False, server_default='10'))
    # Add year and month columns to vacations
    op.add_column('vacations', sa.Column('year', sa.Integer(), nullable=False, server_default='2025'))
    op.add_column('vacations', sa.Column('month', sa.Integer(), nullable=False, server_default='10'))

    # Remove foreign keys and columns referencing payroll_periods
    with op.batch_alter_table('salary_components') as batch_op:
        batch_op.drop_constraint('salary_components_period_id_fkey', type_='foreignkey')
        batch_op.drop_column('period_id')
    with op.batch_alter_table('vacations') as batch_op:
        batch_op.drop_constraint('vacations_period_id_fkey', type_='foreignkey')
        batch_op.drop_column('period_id')

    # Drop payroll_periods table
    op.drop_table('payroll_periods')

    # Add unique constraints
    op.create_unique_constraint('uq_salary_component', 'salary_components', ['employee_id', 'year', 'month', 'type'])
    op.create_unique_constraint('uq_vacation', 'vacations', ['employee_id', 'year', 'month'])

def downgrade():
    # Recreate payroll_periods table
    op.create_table(
        'payroll_periods',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('year', sa.Integer(), nullable=False),
        sa.Column('month', sa.Integer(), nullable=False),
        sa.Column('start_date', sa.Date(), nullable=False),
        sa.Column('end_date', sa.Date(), nullable=False),
        sa.UniqueConstraint('year', 'month', name='uq_period')
    )
    # Remove year and month columns from salary_components and vacations
    op.drop_constraint('uq_salary_component', 'salary_components', type_='unique')
    op.drop_constraint('uq_vacation', 'vacations', type_='unique')
    op.drop_column('salary_components', 'year')
    op.drop_column('salary_components', 'month')
    op.drop_column('vacations', 'year')
    op.drop_column('vacations', 'month')
    # Add period_id columns back
    op.add_column('salary_components', sa.Column('period_id', sa.Integer(), sa.ForeignKey('payroll_periods.id')))
    op.add_column('vacations', sa.Column('period_id', sa.Integer(), sa.ForeignKey('payroll_periods.id')))
