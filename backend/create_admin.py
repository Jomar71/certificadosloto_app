# Contenido completo y corregido para: backend/create_admin.py

import os
import sys
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash
import psycopg2

# Cargar variables de entorno para obtener las credenciales del administrador
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path=dotenv_path)

# Leer credenciales desde variables de entorno, con valores por defecto
ADMIN_USER = os.getenv('ADMIN_USER', 'admin')
ADMIN_PASS = os.getenv('ADMIN_PASS', 'admin123')

def create_admin_user():
    """
    Crea o actualiza el usuario administrador en la base de datos
    utilizando las variables de entorno.
    """
    print(f"Intentando crear/actualizar el usuario administrador '{ADMIN_USER}'...")
    
    db_url = os.getenv('DATABASE_URL')
    if not db_url:
        print("\nERROR: La variable DATABASE_URL no está definida en el archivo .env")
        print("Por favor, asegúrate de que el archivo 'backend/.env' existe y contiene la configuración.")
        return

    try:
        # Conectarse a la base de datos usando la URL del .env
        conn = psycopg2.connect(db_url)
        cur = conn.cursor()

        # Hashear la contraseña para guardarla de forma segura
        hashed_password = generate_password_hash(ADMIN_PASS)

        # 1. Revisar si el usuario ya existe en la tabla 'administradoresloto'
        cur.execute("SELECT id_admin FROM administradoresloto WHERE login_user = %s", (ADMIN_USER,))
        existing_user = cur.fetchone()

        if existing_user:
            # 2a. Si ya existe, actualiza su contraseña
            cur.execute("UPDATE administradoresloto SET login_pass = %s WHERE login_user = %s", (hashed_password, ADMIN_USER))
            print("\n" + "="*50)
            print("¡ÉXITO!")
            print(f"El usuario '{ADMIN_USER}' ya existía.")
            print(f"Su contraseña ha sido actualizada.")
            print("="*50 + "\n")
        else:
            # 2b. Si no existe, lo crea
            cur.execute("INSERT INTO administradoresloto (login_user, login_pass) VALUES (%s, %s)", (ADMIN_USER, hashed_password))
            print("\n" + "="*50)
            print("¡ÉXITO!")
            print(f"Usuario administrador '{ADMIN_USER}' creado correctamente.")
            print("Ahora puedes iniciar sesión con la contraseña configurada en las variables de entorno.")
            print("="*50 + "\n")
        
        # 3. Confirmar y cerrar la conexión
        conn.commit()
        cur.close()
        conn.close()

    except psycopg2.errors.UndefinedTable:
        print("\nERROR: La tabla 'administradoresloto' no existe.")
        print("Asegúrate de haber ejecutado las migraciones de Alembic primero ('alembic upgrade head').")
    except Exception as e:
        print(f"\nOcurrió un error inesperado: {e}")

if __name__ == '__main__':
    create_admin_user()