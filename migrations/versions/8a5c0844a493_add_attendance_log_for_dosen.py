"""Add attendance_log for dosen

Revision ID: 8a5c0844a493
Revises: 82263e118cc6
Create Date: 2025-06-10 01:55:08.346944

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8a5c0844a493'
down_revision: Union[str, None] = '82263e118cc6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'attendance_log',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True, index=True),
        sa.Column('dosen_initial', sa.String, sa.ForeignKey('dosen.alias', ondelete='CASCADE', onupdate='CASCADE'), nullable=False),
        sa.Column('timestamp', sa.DateTime, default=sa.func.now(), nullable=False),
        sa.Column('status_kehadiran', sa.Boolean, nullable=False, default=True),
        sa.Column('keterangan', sa.String, default='', nullable=True)
    )


def downgrade() -> None:
    op.drop_table('attendance_log')
