# ===================================================================================
# ARCHIVO FINAL, COMPLETO Y CORREGIDO PARA: app.py
# Se eliminan las referencias a 'init_pool' para ser compatible con el db.py estable.
# ===================================================================================

import os
import sys
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv

# --- Lógica de importación segura ---
backend_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend')
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

from backend.routes.main import main_bp
from backend.routes.admin import admin_bp
from backend.routes.certificate import certificate_bp
# NO importamos nada de db.py aquí porque no es necesario al inicio

# Carga el archivo .env desde la carpeta 'backend'
dotenv_path = os.path.join(os.path.dirname(__file__), 'backend', '.env')
load_dotenv(dotenv_path=dotenv_path)

def create_app():
    """
    Función factoría para crear la aplicación Flask.
    """
    app = Flask(__name__)

    # --- Configuración de la Aplicación ---
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default-secret-key-de-respaldo')

    # Configuración de CORS para desarrollo y producción
    allowed_origins = [
        "http://127.0.0.1:5500",
        "https://jomar71.github.io"
    ]
    CORS(app, supports_credentials=True, origins=allowed_origins)

    # --- NO hay inicialización de base de datos aquí ---
    # La conexión se manejará individualmente en cada ruta.

    # --- Registrar los Blueprints ---
    app.register_blueprint(main_bp, url_prefix='/api')
    app.register_blueprint(admin_bp, url_prefix='/api')
    app.register_blueprint(certificate_bp, url_prefix='/api')

    return app

# --- Creación y Ejecución de la Aplicación ---
app = create_app()

if __name__ == "__main__":
    # Este bloque se ejecuta cuando corres 'python app.py' desde la raíz
    app.run(debug=True, port=5000)