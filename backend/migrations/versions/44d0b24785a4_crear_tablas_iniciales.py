# Contenido para el nuevo archivo en: backend/migrations/versions/

"""Crear tablas iniciales

Revision ID: (el ID se genera automáticamente)
Revises: 
Create Date: (la fecha se genera automáticamente)

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'manual_initial' # Podemos ponerle un nombre personalizado
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### Comandos para construir las tablas ###
    print("Creando la tabla 'administradores'...")
    op.create_table('administradores',
        sa.Column('admin_id', sa.Integer(), nullable=False),
        sa.Column('login_user', sa.String(length=50), nullable=False),
        sa.Column('login_pass', sa.String(length=255), nullable=False),
        sa.PrimaryKeyConstraint('admin_id'),
        sa.UniqueConstraint('login_user')
    )
    print("Tabla 'administradores' creada.")

    #print("Creando la tabla 'certificadosloto' (si no existe)...")
    # Usamos checkfirst=True para evitar un error si la tabla ya fue creada manualmente
    #op.create_table('certificadosloto',
    #    sa.Column('id_documento', sa.Integer(), nullable=False, autoincrement=True),
    #    sa.Column('tipo_documento', sa.String(length=50), nullable=True),
    #    sa.Column('nombre_persona', sa.String(length=100), nullable=True),
    #    sa.Column('apellido_persona', sa.String(length=100), nullable=True),
    #    sa.Column('numero_identificacion', sa.String(length=50), nullable=False),
    #    sa.Column('fecha_creacion', sa.Date(), nullable=True),
    #    sa.Column('fecha_vencimiento', sa.Date(), nullable=True),
    #    sa.Column('ruta_pdf', sa.String(length=255), nullable=True),
    #    sa.Column('email_persona', sa.String(length=100), nullable=True),
    #   sa.PrimaryKeyConstraint('id_documento'),
    #    sa.UniqueConstraint('numero_identificacion')
    #)
    # print("Tabla 'certificadosloto' creada o ya existente.")
    # ### Fin de los comandos de construcción ###


def downgrade() -> None:
    # ### Comandos para deshacer los cambios (borrar las tablas) ###
    print("Borrando la tabla 'certificadosloto'...")
    op.drop_table('certificadosloto')
    print("Borrando la tabla 'administradores'...")
    op.drop_table('administradores')
    # ### Fin de los comandos de deshacer ###