"""Add MonthInfo (months) dimension table

Revision ID: 20251030_add_monthinfo
Revises: 20251030_integrate_period
Create Date: 2025-10-30

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '20251030_add_monthinfo'
down_revision = '20251030_integrate_period'
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'months',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('year', sa.Integer(), nullable=False),
        sa.Column('month', sa.Integer(), nullable=False),
        sa.Column('working_days', sa.Integer(), nullable=False),
        sa.UniqueConstraint('year', 'month', name='uq_monthinfo')
    )

def downgrade():
    op.drop_table('months')
