"""remove is_active column

Revision ID: f3052ec5bedf
Revises: 28943d3dc459
Create Date: 2025-01-31 03:48:23

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'f3052ec5bedf'
down_revision: Union[str, None] = '28943d3dc459'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # SQLite doesn't support DROP COLUMN, so we need to recreate the table
    with op.batch_alter_table('users') as batch_op:
        batch_op.drop_column('is_active')

def downgrade() -> None:
    with op.batch_alter_table('users') as batch_op:
        batch_op.add_column(sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.text('true')))