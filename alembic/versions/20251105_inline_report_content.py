"""add inline binary content columns to report_files

Revision ID: inline_report_content_20251105
Revises: tz_aware_dt_20251104
Create Date: 2025-11-05
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'inline_report_content_20251105'
down_revision = 'tz_aware_dt_20251104'
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.add_column('report_files', sa.Column('content', sa.LargeBinary(), nullable=True))
    op.add_column('report_files', sa.Column('content_type', sa.String(length=64), nullable=True))
    op.add_column('report_files', sa.Column('size_bytes', sa.Integer(), nullable=True))


def downgrade() -> None:
    op.drop_column('report_files', 'size_bytes')
    op.drop_column('report_files', 'content_type')
    op.drop_column('report_files', 'content')
