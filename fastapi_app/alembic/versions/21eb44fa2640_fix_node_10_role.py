"""Fix Node 10 role

Revision ID: 21eb44fa2640
Revises: 3ac9174dd174
Create Date: 2026-08-17 13:52:16.061386

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '21eb44fa2640'
down_revision: Union[str, Sequence[str], None] = '3ac9174dd174'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("UPDATE nodes SET role = 'Standby' WHERE id = 10 AND role = 'Primary'")


def downgrade() -> None:
    """Downgrade schema."""
    pass
