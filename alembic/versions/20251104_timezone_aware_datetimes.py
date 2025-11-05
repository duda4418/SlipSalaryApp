"""make datetime columns timezone aware (UTC)

Revision ID: tz_aware_dt_20251104
Revises: add_refresh_tokens_table
Create Date: 2025-11-04
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'tz_aware_dt_20251104'
down_revision = 'add_refresh_tokens_table'
branch_labels = None
depends_on = None

# Tables & columns we migrate to timestamptz
_TARGETS = [
    ("employees", "created_at"),
    ("idempotency_keys", "created_at"),
    ("idempotency_keys", "updated_at"),
    ("report_files", "created_at"),
    ("refresh_tokens", "created_at"),
    ("refresh_tokens", "expires_at"),
]

def upgrade() -> None:
    # Convert naive timestamps to timestamptz interpreting existing values as UTC
    for table, col in _TARGETS:
        op.execute(
            f"ALTER TABLE {table} ALTER COLUMN {col} TYPE TIMESTAMP WITH TIME ZONE USING {col} AT TIME ZONE 'UTC'"
        )


def downgrade() -> None:
    # Revert to naive timestamp (values will remain in UTC but lose tz info)
    for table, col in _TARGETS:
        op.execute(
            f"ALTER TABLE {table} ALTER COLUMN {col} TYPE TIMESTAMP WITHOUT TIME ZONE"
        )
