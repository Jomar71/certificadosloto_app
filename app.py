# ===================================================================================
# ARCHIVO COMPLETO Y FINAL PARA: app.py (UBICADO EN LA RAÍZ DEL PROYECTO)
# ===================================================================================

import os
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv

# --- Carga del Archivo .env ---
# Ahora buscamos el archivo .env dentro de la carpeta 'backend'
dotenv_path = os.path.join(os.path.dirname(__file__), 'backend', '.env')
load_dotenv(dotenv_path=dotenv_path)

# --- Importaciones de los Blueprints ---
# Le decimos a Python que busque los módulos dentro del paquete 'backend'
from backend.routes.main import main_bp
from backend.routes.admin import admin_bp
from backend.routes.certificate import certificate_bp
from backend.db import init_pool # Importamos la función para iniciar la conexión a la DB

def create_app():
    """
    Función factoría para crear la aplicación Flask.
    """
    # Especificamos las rutas a las carpetas 'static' y 'templates' del backend
    app = Flask(
        __name__,
        static_folder='backend/static',
        template_folder='backend/templates'
    )

    # --- Configuración de la Aplicación ---
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default-secret-key-de-respaldo')

    # Configuración de CORS para desarrollo y producción
    allowed_origins = [
        "http://127.0.0.1:5500",      # Origen para tu Live Server local
        "https://jomar71.github.io"   # Origen para tu sitio en GitHub Pages
    ]
    CORS(app, supports_credentials=True, origins=allowed_origins)

    # --- Inicializar Conexión a la Base de Datos ---
    # Llamamos a la función que crea el pool de conexiones al arrancar la app
    init_pool()

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