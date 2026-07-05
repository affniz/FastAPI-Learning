"""add foreign-key to posts table

Revision ID: 94162ec7f85d
Revises: 9c3f77926d13
Create Date: 2026-07-05 18:05:27.224439

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '94162ec7f85d'
down_revision: Union[str, Sequence[str], None] = '9c3f77926d13'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts',sa.Column("owner_id",sa.INTEGER(),nullable=False))
    op.create_foreign_key('posts_users_fk',source_table='posts',
                          referent_table='users',local_cols=['owner_id'],
                          remote_cols=['id'],ondelete="CASCADE")
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint('post_user_fk',table_name="posts")
    op.drop_column('posts','owner_id')
    pass
