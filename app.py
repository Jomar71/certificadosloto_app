# ===================================================================================
# ARCHIVO FINAL, COMPLETO Y DEFINITIVO PARA: app.py
# Soluciona el problema de cookies entre dominios para producción.
# ===================================================================================

import os
import sys
from flask import Flask, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv

# NO se importa 'init_pool'
from backend.db import get_db_connection
import subprocess
import time
from werkzeug.security import generate_password_hash

# Carga el archivo .env desde la carpeta 'backend'
dotenv_path = os.path.join(os.path.dirname(__file__), 'backend', '.env')
load_dotenv(dotenv_path=dotenv_path)

def initialize_database():
    """Asegura que las tablas de la BD existan y que haya un admin inicial."""
    print("Inicializando la base de datos...")
    try:
        # Ejecutar Alembic para crear/actualizar tablas
        # Usamos una ruta absoluta para alembic.ini para robustez en Render
        alembic_ini_path = os.path.join(os.path.dirname(__file__), 'backend', 'alembic.ini')
        subprocess.run(['alembic', '-c', alembic_ini_path, 'upgrade', 'head'], check=True)
        print("Migración de Alembic completada.")

        # Crear admin inicial si no existe
        conn = get_db_connection()
        if conn:
            with conn.cursor() as cur:
                admin_user = os.getenv('ADMIN_USER', 'admin')
                cur.execute("SELECT admin_id FROM administradores WHERE login_user = %s", (admin_user,))
                if cur.fetchone() is None:
                    print(f"Creando usuario administrador inicial: {admin_user}")
                    admin_pass = os.getenv('ADMIN_PASS')
                    if not admin_pass:
                        print("ADVERTENCIA: La variable de entorno ADMIN_PASS no está configurada. No se creará el admin.")
                        return
                    
                    hashed_pass = generate_password_hash(admin_pass)
                    cur.execute(
                        "INSERT INTO administradores (login_user, login_pass) VALUES (%s, %s)",
                        (admin_user, hashed_pass)
                    )
                    conn.commit()
                    print("Usuario administrador creado exitosamente.")
                else:
                    print("El usuario administrador ya existe.")
            conn.close()
    except subprocess.CalledProcessError as e:
        print(f"Error durante la migración de Alembic: {e}")
    except Exception as e:
        print(f"Error al inicializar la base de datos: {e}")

def create_app():
    # Configura la carpeta 'frontend' para servir archivos estáticos usando una ruta absoluta.
    # Configura la carpeta estática para que sea la raíz del proyecto
    # Esto es más robusto para Render si los archivos se colocan directamente en la raíz
    project_root = os.path.dirname(os.path.abspath(__file__))
    app = Flask(__name__, static_folder=project_root)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default-secret-key-de-respaldo')

    # --- Configuración de Cookies para Same-Origin (Producción) ---
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
    app.config['SESSION_COOKIE_SECURE'] = True  # Requerido para HTTPS

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

# --- Creación y Ejecución de la Aplicación ---
app = create_app()

# --- Inicialización de la Base de Datos ---
# Esto se ejecuta solo cuando el servidor se inicia, no en cada recarga.
with app.app_context():
    initialize_database()

if __name__ == "__main__":
    port = int(os.getenv('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)