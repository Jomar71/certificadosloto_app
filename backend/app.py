# Contenido COMPLETO y SIMPLIFICADO para: backend/app.py

import os
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv

# Cargar .env desde la carpeta 'backend'
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path=dotenv_path)

# ¡CAMBIO IMPORTANTE! Usamos importaciones directas
from routes.main import main_bp
from routes.admin import admin_bp
from routes.certificate import certificate_bp
# (Asegúrate de que tus archivos de rutas también usen importaciones directas, ej. 'from db import ...')

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default-secret')
    CORS(app, supports_credentials=True, origins="*") # Usamos '*' por ahora
    
    app.register_blueprint(main_bp, url_prefix='/api')
    app.register_blueprint(admin_bp, url_prefix='/api')
    app.register_blueprint(certificate_bp, url_prefix='/api')

    return app

app = create_app()