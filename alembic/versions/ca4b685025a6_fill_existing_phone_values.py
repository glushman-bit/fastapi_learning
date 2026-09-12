"""fill existing phone values

Revision ID: ca4b685025a6
Revises: 2d48a65b1ef3
Create Date: 2026-09-11 18:40:11.140596

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ca4b685025a6'
down_revision: Union[str, Sequence[str], None] = '2d48a65b1ef3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Заполняет phone у существующих пользователей."""
    op.execute(
        sa.text(
            "UPDATE users "
            "SET phone = 'Не указан' "
            "WHERE phone IS NULL"
        )
    )


def downgrade() -> None:
    """Downgrade data migration."""
    pass
