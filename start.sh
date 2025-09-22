#!/bin/bash

# Salir inmediatamente si un comando falla
set -e

# Ejecutar migraciones de la base de datos
echo "Ejecutando migraciones de la base de datos..."
alembic -c backend/alembic.ini upgrade head

# Crear el usuario administrador inicial (si no existe)
echo "Verificando/creando usuario administrador..."
python backend/create_admin.py

# Iniciar la aplicación con Gunicorn
echo "Iniciando la aplicación..."
gunicorn app:app