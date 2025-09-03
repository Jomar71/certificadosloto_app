# ===================================================================================
# ARCHIVO FINAL Y COMPLETO PARA: backend/app.py
# Solución definitiva para CORS que funciona tanto en local como en producción.
# ===================================================================================

import os
import sys
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv

# Lógica de importación segura para que 'python backend/app.py' funcione
if __name__ == "__main__" and __package__ is None:
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    from routes.main import main_bp
    from routes.admin import admin_bp
    from routes.certificate import certificate_bp
else:
    from .routes.main import main_bp
    from .routes.admin import admin_bp
    from .routes.certificate import certificate_bp

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path=dotenv_path)

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default-secret-key')

    # --- ¡¡ESTA ES LA CONFIGURACIÓN DE CORS DEFINITIVA!! ---
    # Una lista de los orígenes en los que confiamos.
    allowed_origins = [
        "http://127.0.0.1:5500",  # Para tu Live Server local
        "https://jomar71.github.io" # Para tu sitio en GitHub Pages
    ]
    
    CORS(
        app,
        supports_credentials=True,
        origins=allowed_origins # Pasamos la lista de orígenes permitidos
    )
    # --------------------------------------------------------
    
    app.register_blueprint(main_bp, url_prefix='/api')
    app.register_blueprint(admin_bp, url_prefix='/api')
    app.register_blueprint(certificate_bp, url_prefix='/api')

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True, port=5000)