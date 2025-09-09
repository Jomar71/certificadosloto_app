# ===================================================================================
# ARCHIVO CORREGIDO PARA: app.py
# Solución optimizada para compatibilidad móvil y cross-domain
# ===================================================================================

import os
import sys
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv

# --- Importación de rutas ---
backend_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend')
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

from backend.routes.main import main_bp
from backend.routes.admin import admin_bp
from backend.routes.certificate import certificate_bp

# Cargar variables de entorno
dotenv_path = os.path.join(os.path.dirname(__file__), 'backend', '.env')
load_dotenv(dotenv_path=dotenv_path)

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default-secret-key')

    # --- CONFIGURACIÓN DE COOKIES OPTIMIZADA PARA MÓVILES ---
    # Configuración más permisiva que funciona mejor en dispositivos móviles
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # Cambio: de 'None' a 'Lax'
    app.config['SESSION_COOKIE_SECURE'] = True
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['PERMANENT_SESSION_LIFETIME'] = 1800  # 30 minutos
    
    # --- CONFIGURACIÓN DE CORS MEJORADA ---
    # Configuración específica para GitHub Pages y desarrollo local
    allowed_origins = [
        "https://jomar71.github.io",  # Tu dominio de GitHub Pages
        "http://127.0.0.1:5500",     # Para desarrollo local
        "http://localhost:5500"       # Alternativa para desarrollo local
    ]
    
    CORS(app, 
         supports_credentials=True, 
         origins=allowed_origins,
         methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
         allow_headers=['Content-Type', 'Authorization', 'X-Requested-With'],
         expose_headers=['Content-Type', 'Authorization']
    )
    
    # --- HEADERS ADICIONALES PARA COMPATIBILIDAD ---
    @app.after_request
    def after_request(response):
        # Headers específicos para mejor compatibilidad móvil
        origin = request.headers.get('Origin')
        if origin in allowed_origins:
            response.headers['Access-Control-Allow-Origin'] = origin
            response.headers['Access-Control-Allow-Credentials'] = 'true'
        
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization,X-Requested-With'
        response.headers['Access-Control-Allow-Methods'] = 'GET,PUT,POST,DELETE,OPTIONS'
        
        # Headers de seguridad y rendimiento
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        
        return response
    
    # --- MANEJO DE PREFLIGHT REQUESTS ---
    @app.before_request
    def handle_preflight():
        from flask import request
        if request.method == "OPTIONS":
            response = make_response()
            response.headers.add("Access-Control-Allow-Origin", "*")
            response.headers.add('Access-Control-Allow-Headers', "*")
            response.headers.add('Access-Control-Allow-Methods', "*")
            return response

    # --- REGISTRO DE BLUEPRINTS ---
    app.register_blueprint(main_bp, url_prefix='/api')
    app.register_blueprint(admin_bp, url_prefix='/api')
    app.register_blueprint(certificate_bp, url_prefix='/api')

    # --- RUTA DE HEALTH CHECK ---
    @app.route('/health')
    def health_check():
        return {'status': 'ok', 'message': 'API funcionando correctamente'}, 200
    
    # --- RUTA RAÍZ INFORMATIVA ---
    @app.route('/')
    def root():
        return {
            'message': 'API de Certificados',
            'version': '1.0',
            'endpoints': ['/api/certificates', '/api/admin', '/health']
        }, 200

    return app

# Importar make_response y request para el manejo de CORS
from flask import make_response, request

app = create_app()

# --- CONFIGURACIÓN PARA PRODUCCIÓN ---
if __name__ == "__main__":
    # Solo se ejecuta en desarrollo local
    app.run(debug=True, port=5000, host='0.0.0.0')