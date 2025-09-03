# Contenido COMPLETO y CORREGIDO para: wsgi.py

import sys
import os

# Directorio del backend
backend_dir = os.path.join(os.path.dirname(__file__), 'backend')

# Añade el directorio del backend al path de Python
sys.path.insert(0, backend_dir)

# ¡NUEVA LÍNEA! Cambia el directorio de trabajo actual al del backend
os.chdir(backend_dir)

# Ahora, importa la aplicación 'app' desde el archivo 'app.py' (que ahora está en el path)
from app import app

# Gunicorn busca esta variable 'application'
application = app