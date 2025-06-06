"""add google user

Revision ID: dda0a8c1fe23
Revises: 825e19d5ae0d
Create Date: 2025-06-01 14:09:14.121393

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dda0a8c1fe23'
down_revision: Union[str, None] = '825e19d5ae0d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('profile_picture_url', sa.String(), nullable=True))
    op.add_column('users', sa.Column('external', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'external')
    op.drop_column('users', 'profile_picture_url')
    # ### end Alembic commands ###
