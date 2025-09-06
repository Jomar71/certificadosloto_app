# ===================================================================================
# ARCHIVO FINAL Y COMPLETO PARA: app.py
# Solución definitiva para el manejo de cookies entre dominios en producción.
# ===================================================================================

import os
import sys
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv

# --- (La lógica de importación se queda igual) ---
backend_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend')
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)
from backend.routes.main import main_bp
from backend.routes.admin import admin_bp
from backend.routes.certificate import certificate_bp
from backend.db import init_pool

dotenv_path = os.path.join(os.path.dirname(__file__), 'backend', '.env')
load_dotenv(dotenv_path=dotenv_path)

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default-secret-key')

    # --- ¡¡ESTA ES LA CONFIGURACIÓN DE COOKIES DEFINITIVA!! ---
    # Para producción, le decimos al navegador que las cookies son seguras
    app.config['SESSION_COOKIE_SAMESITE'] = 'None'
    app.config['SESSION_COOKIE_SECURE'] = True
    # -----------------------------------------------------------

    # --- Configuración de CORS ---
    allowed_origins = [
        "http://127.0.0.1:5500",
        "https://jomar71.github.io"
    ]
    CORS(app, supports_credentials=True, origins=allowed_origins)
    
    init_pool()
    
    app.register_blueprint(main_bp, url_prefix='/api')
    app.register_blueprint(admin_bp, url_prefix='/api')
    app.register_blueprint(certificate_bp, url_prefix='/api')

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True, port=5000)