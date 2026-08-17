"""fix index and add lease token

Revision ID: 5f1b2c3d4e5f
Revises: 44cb8bcea472
Create Date: 2026-08-17 17:35:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5f1b2c3d4e5f'
down_revision: Union[str, None] = '44cb8bcea472'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Drop the incorrect index that was created in the previous migration without sqlite_where
    with op.batch_alter_table('sync_jobs', schema=None) as batch_op:
        # Drop the old index (we drop it without where clauses to be safe on SQLite and Postgres)
        batch_op.drop_index('ix_sync_jobs_active')
        
    # 2. Re-create the index correctly with both postgresql_where and sqlite_where
    with op.batch_alter_table('sync_jobs', schema=None) as batch_op:
        batch_op.create_index(
            'ix_sync_jobs_active', 
            ['project_id'], 
            unique=True, 
            postgresql_where=sa.text("status NOT IN ('SUCCESS', 'FAILED')"),
            sqlite_where=sa.text("status NOT IN ('SUCCESS', 'FAILED')")
        )

    # 3. Add lease_token column for strict fencing
    with op.batch_alter_table('sync_jobs', schema=None) as batch_op:
        batch_op.add_column(sa.Column('lease_token', sa.String(length=36), nullable=True))


def downgrade() -> None:
    with op.batch_alter_table('sync_jobs', schema=None) as batch_op:
        batch_op.drop_column('lease_token')
        batch_op.drop_index('ix_sync_jobs_active', postgresql_where=sa.text("status NOT IN ('SUCCESS', 'FAILED')"), sqlite_where=sa.text("status NOT IN ('SUCCESS', 'FAILED')"))
        batch_op.create_index('ix_sync_jobs_active', ['project_id'], unique=True, postgresql_where=sa.text("status NOT IN ('SUCCESS', 'FAILED')"))
