#!/bin/bash

# Salir inmediatamente si un comando falla
set -e

# Cambiar al directorio del backend
cd backend

# Ejecutar migraciones de la base de datos desde el directorio del backend
echo "Ejecutando migraciones de la base de datos..."
alembic -c alembic.ini upgrade head

# Crear el usuario administrador inicial (si no existe)
echo "Verificando/creando usuario administrador..."
python create_admin.py

# Volver al directorio raíz e iniciar la aplicación con Gunicorn
echo "Iniciando la aplicación..."
cd ..
gunicorn app:app