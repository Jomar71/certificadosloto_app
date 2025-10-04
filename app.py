# ===================================================================================
# ARCHIVO FINAL, COMPLETO Y DEFINITIVO PARA: app.py
# Soluciona el problema de cookies entre dominios para producción.
# ===================================================================================

import os
import sys
from flask import Flask, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash

# Se importan las funciones necesarias de la base de datos
from backend.db import get_db_connection, release_db_connection

# Carga el archivo .env desde la carpeta 'backend'
dotenv_path = os.path.join(os.path.dirname(__file__), 'backend', '.env')
load_dotenv(dotenv_path=dotenv_path)

def create_app():
    # Configura la carpeta 'frontend' para servir archivos estáticos usando una ruta absoluta.
    # Configura la carpeta estática para que sea la raíz del proyecto
    # Esto es más robusto para Render si los archivos se colocan directamente en la raíz
    project_root = os.path.dirname(os.path.abspath(__file__))
    app = Flask(__name__, static_folder=project_root)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default-secret-key-de-respaldo')

    # --- Configuración de Cookies para Same-Origin (Producción) ---
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
    app.config['SESSION_COOKIE_SECURE'] = not app.debug  # True solo en producción (HTTPS)

    # --- Configuración de CORS ---
    # Permite credenciales (cookies) y acepta peticiones de cualquier origen.
    # Esta es la configuración más compatible para producción cuando el frontend y backend están unificados.
    CORS(app, supports_credentials=True, origins="*")

    # --- Registrar los Blueprints de la API ---
    # Importar blueprints dentro de la función para asegurar el registro en entornos de despliegue
    from backend.routes.main import main_bp
    from backend.routes.admin import admin_bp
    from backend.routes.certificate import certificate_bp

    app.register_blueprint(main_bp, url_prefix='/api/auth')      # Rutas de autenticación
    app.register_blueprint(admin_bp, url_prefix='/api/admin')      # Rutas de administración
    app.register_blueprint(certificate_bp, url_prefix='/api/certificates') # Rutas públicas de certificados

    # --- Rutas para servir el Frontend ---
    # Sirve el index.html para la ruta raíz y cualquier otra ruta no-API.
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve_frontend(path):
        # Intenta servir el archivo desde la carpeta 'frontend'
        frontend_path = os.path.join(project_root, 'frontend', path)
        if os.path.exists(frontend_path) and os.path.isfile(frontend_path):
            return send_from_directory(os.path.join(project_root, 'frontend'), path)
        
        # Si no se encuentra en 'frontend', intenta servirlo desde la raíz del proyecto
        root_path = os.path.join(project_root, path)
        if os.path.exists(root_path) and os.path.isfile(root_path):
            return send_from_directory(project_root, path)

        # Si no es un archivo, o no se encuentra, sirve el index.html (comportamiento de SPA)
        return send_from_directory(os.path.join(project_root, 'frontend'), 'index.html')

    return app

# --- Función para Inicializar la Base de Datos ---
def init_db():
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # Crear la tabla de administradores si no existe
        cur.execute("""
            CREATE TABLE IF NOT EXISTS administradoresloto (
                id_admin SERIAL PRIMARY KEY,
                login_user VARCHAR(255) UNIQUE NOT NULL,
                login_pass VARCHAR(255) NOT NULL
            );
        """)

        # Verificar si ya existe algún administrador
        cur.execute("SELECT COUNT(*) FROM administradoresloto")
        if cur.fetchone()[0] == 0:
            # Insertar un administrador por defecto si la tabla está vacía
            hashed_password = generate_password_hash('password')
            cur.execute(
                "INSERT INTO administradoresloto (login_user, login_pass) VALUES (%s, %s)",
                ('admin', hashed_password)
            )
            print("Tabla 'administradoresloto' creada y administrador por defecto insertado.")
        
        conn.commit()
        cur.close()
    except Exception as e:
        print(f"Error al inicializar la base de datos: {e}")
    finally:
        if conn:
            release_db_connection(conn)

# --- Creación y Ejecución de la Aplicación ---
app = create_app()

# --- Inicializar la Base de Datos al Arrancar ---
with app.app_context():
    init_db()

if __name__ == "__main__":
    port = int(os.getenv('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)