"""add phone and email to users

Revision ID: 8bec7a570ab7
Revises: c6f9bb70c315
Create Date: 2026-11-11 14:04:06.487400

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8bec7a570ab7'
down_revision: Union[str, Sequence[str], None] = 'c6f9bb70c315'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None



def upgrade() -> None:
    op.add_column(
        'users',
        sa.Column('phone', sa.String(length=20), nullable=True)
    )
    op.add_column(
        'users',
        sa.Column('email', sa.String(length=254), nullable=True)
    )

    op.create_index(
        'ix_users_phone',
        'users',
        ['phone'],
        unique=True
    )
    op.create_index(
        'ix_users_email',
        'users',
        ['email'],
        unique=True
    )


def downgrade() -> None:
    op.drop_index('ix_users_email', table_name='users')
    op.drop_index('ix_users_phone', table_name='users')
    op.drop_column('users', 'email')
    op.drop_column('users', 'phone')

