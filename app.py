# ===================================================================================
# ARCHIVO FINAL, COMPLETO Y DEFINITIVO PARA: app.py
# Soluciona el problema de cookies entre dominios para producción.
# ===================================================================================

import os
import sys
from flask import Flask, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv

# --- Lógica de importación segura ---
backend_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend')
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

from backend.routes.main import main_bp
from backend.routes.admin import admin_bp
from backend.routes.certificate import certificate_bp
# NO se importa 'init_pool'
from backend.db import get_db_connection

# Carga el archivo .env desde la carpeta 'backend'
dotenv_path = os.path.join(os.path.dirname(__file__), 'backend', '.env')
load_dotenv(dotenv_path=dotenv_path)

def create_app():
    app = Flask(__name__, static_folder='../frontend', static_url_path='/')
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default-secret-key-de-respaldo')

    # --- ¡¡ESTA ES LA CONFIGURACIÓN DE COOKIES DEFINITIVA!! ---
    # Para producción (HTTPS), le decimos al navegador que las cookies son seguras
    # y que pueden ser enviadas entre diferentes sitios (None).
    app.config['SESSION_COOKIE_SAMESITE'] = 'None'
    app.config['SESSION_COOKIE_SECURE'] = True
    # ¡IMPORTANTE! Especifica el dominio para que las cookies funcionen en Render.
    app.config['SESSION_COOKIE_DOMAIN'] = '.certificadosloto-app.onrender.com'
    # -----------------------------------------------------------
    
    # --- Configuración de CORS ---
    # Ahora que todo se sirve desde el mismo dominio, solo necesitamos permitir nuestro propio origen.
    allowed_origins = [
        "https://certificadosloto-app.onrender.com"
    ]
    CORS(app, supports_credentials=True, origins=allowed_origins)
    
    # --- Registrar los Blueprints ---
    app.register_blueprint(main_bp, url_prefix='/api')
    app.register_blueprint(admin_bp, url_prefix='/api')
    app.register_blueprint(certificate_bp, url_prefix='/api')

    # --- Sirviendo el frontend ---
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve(path):
        if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
            return send_from_directory(app.static_folder, path)
        else:
            return send_from_directory(app.static_folder, 'index.html')

    return app

# --- Creación y Ejecución de la Aplicación ---
app = create_app()

if __name__ == "__main__":
    app.run(debug=True, port=5000)