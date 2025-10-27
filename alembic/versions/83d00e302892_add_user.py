"""add user

Revision ID: 83d00e302892
Revises: 
Create Date: 2025-10-27 08:41:54.849450

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '83d00e302892'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('users',
    sa.Column('first_name', sa.String(length=255), nullable=False),
    sa.Column('last_name', sa.String(length=255), nullable=False),
    sa.Column('second_name', sa.String(length=255), nullable=True),
    sa.Column('email', sa.String(length=320), nullable=False),
    sa.Column('hashed_password', sa.String(length=1024), nullable=False),
    sa.Column('role', sa.Enum('READER', 'LIBRARIAN', 'ADMINISTRATOR', 'SUPERVISOR', name='userrole'), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('is_superuser', sa.Boolean(), nullable=False),
    sa.Column('is_verified', sa.Boolean(), nullable=False),
    sa.Column('uid', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('uid', name=op.f('pk_users'))
    )
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_users_email'), ['email'], unique=True)
        batch_op.create_index(batch_op.f('ix_users_first_name'), ['first_name'], unique=False)
        batch_op.create_index(batch_op.f('ix_users_last_name'), ['last_name'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_users_last_name'))
        batch_op.drop_index(batch_op.f('ix_users_first_name'))
        batch_op.drop_index(batch_op.f('ix_users_email'))

    op.drop_table('users')
