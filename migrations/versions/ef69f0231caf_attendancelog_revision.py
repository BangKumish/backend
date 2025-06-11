"""AttendanceLog revision

Revision ID: ef69f0231caf
Revises: 8a5c0844a493
Create Date: 2025-06-10 14:55:21.806617

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ef69f0231caf'
down_revision: Union[str, None] = '8a5c0844a493'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_table('attendance_log')
    op.create_table(
        'attendance_log',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True, index=True),
        sa.Column('dosen_inisial', sa.String, sa.ForeignKey('dosen.alias', ondelete='CASCADE', onupdate='CASCADE'), nullable=False),
        sa.Column('dosen_nama', sa.String, nullable=False),
        sa.Column('tanggal', sa.Date, default=sa.func.current_date(), nullable=False),
        sa.Column('status_kehadiran', sa.Boolean, nullable=False, default=True),
        sa.Column('keterangan', sa.String, default='', nullable=True)
    )


def downgrade() -> None:
    op.drop_table('attendance_log')
