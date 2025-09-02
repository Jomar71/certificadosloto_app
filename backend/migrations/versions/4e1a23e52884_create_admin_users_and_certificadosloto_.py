"""create admin_users and certificadosloto tables

Revision ID: 4e1a23e52884
Revises: 
Create Date: 2025-08-24 00:42:21.557500

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4e1a23e52884'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'admin_users',
        sa.Column('admin_id', sa.Integer, primary_key=True),
        sa.Column('login_user', sa.String(80), unique=True, nullable=False),
        sa.Column('login_pass', sa.String(128), nullable=False)
    )
    op.create_table(
        'certificadosloto',
        sa.Column('id_documento', sa.Integer, primary_key=True),
        sa.Column('tipo_documento', sa.String(50), nullable=False),
        sa.Column('nombre_persona', sa.String(100), nullable=False),
        sa.Column('apellido_persona', sa.String(100), nullable=False),
        sa.Column('numero_identificacion', sa.String(20), unique=True, nullable=False),
        sa.Column('fecha_creacion', sa.Date, nullable=False),
        sa.Column('fecha_vencimiento', sa.Date, nullable=False),
        sa.Column('ruta_pdf', sa.String(255)),
        sa.Column('email_persona', sa.String(120))
    )


def downgrade() -> None:
    op.drop_table('certificadosloto')
    op.drop_table('admin_users')