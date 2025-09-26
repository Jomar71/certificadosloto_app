import os
import sys
from werkzeug.security import generate_password_hash
from dotenv import load_dotenv

# Añadir el directorio raíz del proyecto al sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.db import get_db_connection, release_db_connection

def update_admin_passwords():
    """
    Actualiza todas las contraseñas de los administradores en la tabla
    'administradoresloto' a un formato hasheado.
    """
    conn = None
    try:
        # Cargar variables de entorno desde el archivo .env en la carpeta backend
        dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
        load_dotenv(dotenv_path=dotenv_path)

        conn = get_db_connection()
        if not conn:
            print("Error: No se pudo establecer conexión con la base de datos.")
            return

        cur = conn.cursor()

        # 1. Obtener todos los administradores con contraseñas en texto plano
        cur.execute("SELECT id_admin, login_pass FROM administradoresloto")
        admins_to_update = []
        for admin in cur.fetchall():
            id_admin, plain_password = admin
            # Verificar si la contraseña parece ya hasheada (los hashes de werkzeug suelen empezar con 'pbkdf2:sha256')
            if not plain_password.startswith('pbkdf2:sha256'):
                admins_to_update.append(admin)

        if not admins_to_update:
            print("No hay contraseñas en texto plano para actualizar. Proceso finalizado.")
            return

        print(f"Se encontraron {len(admins_to_update)} administradores con contraseñas en texto plano para actualizar.")

        # 2. Recorrer los administradores y actualizar cada contraseña
        for id_admin, plain_password in admins_to_update:
            print(f"Actualizando contraseña para el administrador con ID: {id_admin}...")
            hashed_password = generate_password_hash(plain_password)
            
            cur.execute(
                "UPDATE administradoresloto SET login_pass = %s WHERE id_admin = %s",
                (hashed_password, id_admin)
            )

        # 3. Confirmar los cambios
        conn.commit()
        print(f"\n¡Éxito! Se han actualizado {len(admins_to_update)} contraseñas de administradores.")

    except Exception as e:
        print(f"\nOcurrió un error durante la actualización: {e}")
        if conn:
            conn.rollback()
    finally:
        if conn:
            cur.close()
            release_db_connection(conn)
            print("Conexión con la base de datos cerrada.")

if __name__ == "__main__":
    update_admin_passwords()