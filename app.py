# ===================================================================================
# ARCHIVO FINAL, COMPLETO Y CORREGIDO PARA: app.py
# Se restaura el bloque de arranque para la ejecución local.
# ===================================================================================
import os
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv

# Carga el .env desde la carpeta backend
dotenv_path = os.path.join(os.path.dirname(__file__), 'backend', '.env')
load_dotenv(dotenv_path=dotenv_path)

# Importamos los módulos
from backend.routes.main import main_bp
from backend.routes.admin import admin_bp
from backend.routes.certificate import certificate_bp
from backend.db import get_db_connection

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'un-secreto-muy-seguro')

# --- CONFIGURACIÓN DE CORS DEFINITIVA ---
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
    return "El servidor backend de certificados está funcionando."

# --- ¡¡ESTE ES EL BLOQUE QUE FALTABA!! ---
# Permite que el servidor se inicie cuando ejecutas 'python app.py'
if __name__ == "__main__":
    app.run(debug=True, port=5000)
# -----------------------------------------