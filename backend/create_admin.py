# Contenido completo y corregido para: backend/create_admin.py

import os
import sys
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash
import psycopg2

# --- Configuración ---
# Puedes cambiar estos valores al nombre de usuario y contraseña que prefieras
NEW_ADMIN_USER = "admin"
NEW_ADMIN_PASS = "admin123" # Te sugiero usar una contraseña un poco más segura
# ---------------------

# Añadir el directorio raíz del proyecto al path de Python para encontrar módulos
# Esto es necesario para poder llamar a este script desde la raíz
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

# Ahora cargamos las variables de entorno que están en la raíz
# El archivo .env debe estar en la carpeta 'backend/'
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path=dotenv_path)


def create_admin_user():
    """
    Crea o actualiza el usuario administrador en la base de datos.
    """
    print(f"Intentando crear/actualizar el usuario administrador '{NEW_ADMIN_USER}'...")
    
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
        hashed_password = generate_password_hash(NEW_ADMIN_PASS)

        # 1. Revisar si el usuario ya existe en la tabla 'administradores'
        cur.execute("SELECT admin_id FROM administradores WHERE login_user = %s", (NEW_ADMIN_USER,))
        existing_user = cur.fetchone()

        if existing_user:
            # 2a. Si ya existe, actualiza su contraseña
            cur.execute("UPDATE administradores SET login_pass = %s WHERE login_user = %s", (hashed_password, NEW_ADMIN_USER))
            print("\n" + "="*50)
            print("¡ÉXITO!")
            print(f"El usuario '{NEW_ADMIN_USER}' ya existía.")
            print(f"Su contraseña ha sido actualizada a: '{NEW_ADMIN_PASS}'")
            print("="*50 + "\n")
        else:
            # 2b. Si no existe, lo crea
            cur.execute("INSERT INTO administradores (login_user, login_pass) VALUES (%s, %s)", (NEW_ADMIN_USER, hashed_password))
            print("\n" + "="*50)
            print("¡ÉXITO!")
            print(f"Usuario administrador '{NEW_ADMIN_USER}' creado correctamente.")
            print(f"Ahora puedes iniciar sesión con la contraseña: '{NEW_ADMIN_PASS}'")
            print("="*50 + "\n")
        
        # 3. Confirmar y cerrar la conexión
        conn.commit()
        cur.close()
        conn.close()

    except psycopg2.errors.UndefinedTable:
        print("\nERROR: La tabla 'administradores' no existe.")
        print("Asegúrate de haber ejecutado las migraciones de Alembic primero ('alembic upgrade head').")
    except Exception as e:
        print(f"\nOcurrió un error inesperado: {e}")

if __name__ == '__main__':
    create_admin_user()