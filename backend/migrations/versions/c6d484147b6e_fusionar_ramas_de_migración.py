"""Fusionar ramas de migración

Revision ID: c6d484147b6e
Revises: manual_initial, 4e1a23e52884
Create Date: 2025-08-26 23:31:25.287458

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c6d484147b6e'
down_revision: Union[str, Sequence[str], None] = ('manual_initial', '4e1a23e52884')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
