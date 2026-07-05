"""add content column to posts table

Revision ID: 9743fbd7376b
Revises: a8bf0633d9ad
Create Date: 2026-07-05 17:48:34.078825

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9743fbd7376b'
down_revision: Union[str, Sequence[str], None] = 'a8bf0633d9ad'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts',sa.Column('content',sa.String(),nullable=False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts','content')
    pass
