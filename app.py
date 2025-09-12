# ===================================================================================
# ARCHIVO FINAL, COMPLETO Y DEFINITIVO PARA: app.py
# ===================================================================================
import os
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv

# Carga el .env desde la carpeta backend
dotenv_path = os.path.join(os.path.dirname(__file__), 'backend', '.env')
load_dotenv(dotenv_path=dotenv_path)

# Importamos los módulos DESPUÉS de cargar el .env
from backend.routes.main import main_bp
from backend.routes.admin import admin_bp
from backend.routes.certificate import certificate_bp
from backend.db import get_db_connection

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'un-secreto-muy-seguro')

# --- CONFIGURACIÓN DE CORS DEFINITIVA ---
# Permite explícitamente tu sitio de GitHub Pages y tu entorno local
CORS(
    app,
    origins=["https://jomar71.github.io", "http://127.0.0.1:5500"],
    supports_credentials=True
)
# ----------------------------------------

# Registrar los Blueprints
app.register_blueprint(main_bp, url_prefix='/api')
app.register_blueprint(admin_bp, url_prefix='/api')
app.register_blueprint(certificate_bp, url_prefix='/api')

@app.route('/')
def index():
    # Una ruta simple para verificar que el servidor está vivo
    return "El servidor backend de certificados está funcionando."

# No necesitamos el bloque if __name__ == "__main__" para Render