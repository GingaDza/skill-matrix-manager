"""merge migrations

Revision ID: merge_migration_20250131
Revises: 6009b63a280a, f3052ec5bedf
Create Date: 2025-01-31 04:07:22

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'merge_migration_20250131'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: tuple[str, str] = ('6009b63a280a', 'f3052ec5bedf')

def upgrade() -> None:
    pass

def downgrade() -> None:
    pass