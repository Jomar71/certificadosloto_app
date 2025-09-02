# Contenido completo y corregido para: backend/migrations/env.py

import os
from logging.config import fileConfig

# --- ¡CAMBIO 1: IMPORTAMOS dotenv! ---
from dotenv import load_dotenv

from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context

# --- ¡CAMBIO 2: CARGAMOS EL ARCHIVO .env! ---
# Esta sección busca el archivo .env en la carpeta 'backend/' y carga la DATABASE_URL.
# Sube un nivel desde 'migrations' (donde está este archivo) a 'backend'.
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path=dotenv_path)
# ---------------------------------------------

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# --- ¡CAMBIO 3: LE DAMOS LA URL A ALEMBIC DESDE EL PRINCIPIO! ---
# Esta es la línea más importante. Le decimos a Alembic que use la variable
# de entorno 'DATABASE_URL' que acabamos de cargar del archivo .env.
# Esto sobreescribe cualquier cosa que esté en el archivo alembic.ini.
config.set_main_option('sqlalchemy.url', os.getenv('DATABASE_URL'))
# ---------------------------------------------

# Interpret the config file for Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
target_metadata = None

# ... (el resto del archivo no necesita cambios, pero lo incluyo para que esté completo)

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()