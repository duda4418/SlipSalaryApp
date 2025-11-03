"""add refresh_tokens table

Revision ID: add_refresh_tokens_table
Revises: 20251030_new_model_structure
Create Date: 2025-11-03
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

# revision identifiers, used by Alembic.
revision = 'add_refresh_tokens_table'
down_revision = '20251030_new_model_structure'
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.create_table(
        'refresh_tokens',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('employee_id', UUID(as_uuid=True), sa.ForeignKey('employees.id', ondelete='CASCADE'), nullable=False),
        sa.Column('token_hash', sa.String(255), nullable=False, unique=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.Column('expires_at', sa.DateTime(), nullable=False),
        sa.Column('revoked', sa.Boolean(), nullable=False, server_default=sa.text('false')),
        sa.Column('replaced_by', UUID(as_uuid=True), sa.ForeignKey('refresh_tokens.id', ondelete='SET NULL'), nullable=True),
    )
    # Create index explicitly (avoid duplicate via index=True param)
    op.create_index('ix_refresh_tokens_employee_id', 'refresh_tokens', ['employee_id'])


def downgrade() -> None:
    op.drop_index('ix_refresh_tokens_employee_id', table_name='refresh_tokens')
    op.drop_table('refresh_tokens')
