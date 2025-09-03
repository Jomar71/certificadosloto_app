# Contenido para el archivo raíz: wsgi.py
import sys
import os

# Añade la carpeta 'backend' al path de Python
# para que pueda encontrar los módulos como 'routes', 'db', etc.
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

# Ahora, importa la aplicación 'app' desde el archivo 'backend/app.py'
from app import app

# Si se ejecuta directamente, gunicorn usará esta variable 'application'
application = app