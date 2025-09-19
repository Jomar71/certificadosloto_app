# ===================================================================================
# ARCHIVO FINAL, COMPLETO Y DEFINITIVO PARA: app.py
# Soluciona el problema de cookies entre dominios para producción.
# ===================================================================================

import os
import sys
from flask import Flask, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv

from backend.routes.main import main_bp
from backend.routes.admin import admin_bp
from backend.routes.certificate import certificate_bp
# NO se importa 'init_pool'
from backend.db import get_db_connection

# Carga el archivo .env desde la carpeta 'backend'
dotenv_path = os.path.join(os.path.dirname(__file__), 'backend', '.env')
load_dotenv(dotenv_path=dotenv_path)

def create_app():
    # Configura la carpeta 'frontend' para servir archivos estáticos usando una ruta absoluta.
    frontend_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'frontend')
    app = Flask(__name__, static_folder=frontend_folder)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default-secret-key-de-respaldo')

    # --- Configuración de Cookies para Same-Origin (Producción) ---
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
    app.config['SESSION_COOKIE_SECURE'] = True  # Requerido para HTTPS

    # --- Configuración de CORS ---
    # Permite credenciales (cookies) y acepta peticiones de cualquier origen.
    # Esta es la configuración más compatible para producción cuando el frontend y backend están unificados.
    CORS(app, supports_credentials=True, origins="*")

    # --- Registrar los Blueprints de la API ---
    app.register_blueprint(main_bp, url_prefix='/api/auth')      # Rutas de autenticación
    app.register_blueprint(admin_bp, url_prefix='/api/admin')      # Rutas de administración
    app.register_blueprint(certificate_bp, url_prefix='/api/certificates') # Rutas públicas de certificados

    # --- Rutas para servir el Frontend ---
    # Sirve el index.html para la ruta raíz y cualquier otra ruta no-API.
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve_frontend(path):
        # Construye la ruta al archivo solicitado
        requested_path = os.path.join(app.static_folder, path)

        # Si el path es un archivo que existe, lo sirve.
        if path != "" and os.path.exists(requested_path):
            return send_from_directory(app.static_folder, path)
        # Si no, sirve el index.html (comportamiento de SPA).
        else:
            return send_from_directory(app.static_folder, 'index.html')

    return app

# --- Creación y Ejecución de la Aplicación ---
app = create_app()

if __name__ == "__main__":
    app.run(debug=True, port=5000)