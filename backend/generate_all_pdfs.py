# ===================================================================================
# ARCHIVO FINAL Y COMPLETO PARA: backend/generate_all_pdfs.py
# Soluciona los problemas de importación y de contexto de la aplicación.
# ===================================================================================

import os
import sys
from dotenv import load_dotenv
from datetime import datetime

# --- Configuración para que el script encuentre los otros módulos ---
# Añade la carpeta raíz del proyecto al path de Python
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)
# Carga el archivo .env desde la carpeta 'backend'
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path=dotenv_path)
# --------------------------------------------------------------------

# Ahora que el path está configurado, podemos importar los módulos del backend
from backend.db import get_db_connection, release_db_connection
from backend.pdf_generator import generate_certificate_pdf
from flask import Flask

def process_all_pdfs(force_update=False):
    """
    Recorre la base de datos, encuentra certificados sin PDF,
    los genera y actualiza el registro.
    """
    # Necesitamos crear una 'app' de Flask falsa para que el generador de PDF
    # tenga el 'contexto de aplicación' necesario para encontrar la carpeta 'static'.
    app = Flask(__name__, root_path=os.path.dirname(os.path.abspath(__file__)))
    
    with app.app_context():
        print("--- INICIANDO SCRIPT DE GESTIÓN DE PDFS ---")
        
        conn, cur = None, None
        try:
            conn = get_db_connection()
            cur = conn.cursor()

            # --- LÓGICA DE SELECCIÓN ---
            if force_update:
                print(">>> MODO DE ACTUALIZACIÓN FORZADA ACTIVADO <<<")
                print("Se regenerarán los PDFs para TODOS los certificados.")
                cur.execute("SELECT * FROM certificadosloto")
            else:
                print(">>> MODO NORMAL ACTIVADO <<<")
                print("Se generarán PDFs solo para certificados nuevos (sin PDF asociado).")
                cur.execute("SELECT * FROM certificadosloto WHERE ruta_pdf IS NULL OR ruta_pdf = ''")
            # ---------------------------

            certificates_to_process = cur.fetchall()
            
            if not certificates_to_process:
                print("¡No hay certificados que procesar según el modo seleccionado!")
                return

            print(f"Se encontraron {len(certificates_to_process)} certificados para procesar...")
            
            count_success = 0
            count_fail = 0

            # Recorrer cada certificado encontrado
            for cert_row in certificates_to_process:
                # Convertir la fila de la base de datos en un diccionario
                cert_data = {
                    "id_documento": cert_row[0], "tipo_documento": cert_row[1],
                    "nombre_persona": cert_row[2], "apellido_persona": cert_row[3],
                    "numero_identificacion": cert_row[4], "fecha_creacion": cert_row[5],
                    "fecha_vencimiento": cert_row[6], "email_persona": cert_row[8]
                }
                
                cert_id = cert_data['id_documento']
                print(f"Procesando certificado ID: {cert_id} - {cert_data['nombre_persona']}...")

                # Llamar a la función para generar el PDF
                pdf_filename = generate_certificate_pdf(cert_data)

                if pdf_filename:
                    # Si el PDF se creó, actualizar la base de datos con su nombre
                    update_cur = conn.cursor()
                    update_cur.execute("UPDATE certificadosloto SET ruta_pdf = %s WHERE id_documento = %s", (pdf_filename, cert_id))
                    conn.commit()
                    update_cur.close()
                    print(f" -> ÉXITO: PDF '{pdf_filename}' generado y registro actualizado.")
                    count_success += 1
                else:
                    print(f" -> FALLO: No se pudo generar el PDF para el certificado ID: {cert_id}.")
                    count_fail += 1
            
            print("\n--- PROCESO FINALIZADO ---")
            print(f"PDFs generados exitosamente: {count_success}")
            print(f"Fallos: {count_fail}")

        except Exception as e:
            print(f"\nOcurrió un error crítico durante el proceso: {e}")
        finally:
            if cur: cur.close()
            if conn: release_db_connection(conn)

if __name__ == '__main__':
    # --- CÓMO EJECUTAR ---
    # Para generar solo los nuevos: python backend/generate_all_pdfs.py
    # Para forzar la actualización de TODOS: python backend/generate_all_pdfs.py force
    # -----------------------
    force = len(sys.argv) > 1 and sys.argv[1] == 'force'
    process_all_pdfs(force_update=force)