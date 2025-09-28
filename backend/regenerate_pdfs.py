import os
import sys
import traceback

# Añadir el directorio raíz del proyecto al sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.db import get_db_connection, release_db_connection
from backend.pdf_generator import generate_certificate_pdf

def regenerate_all_pdfs():
    """
    Recorre todos los certificados en la base de datos,
    regenera sus archivos PDF y actualiza la ruta en la base de datos.
    """
    conn = None
    try:
        conn = get_db_connection()
        if not conn:
            print("Error crítico: No se pudo conectar a la base de datos.")
            return

        cur = conn.cursor()
        
        # 1. Obtener todos los datos de los certificados existentes
        cur.execute("SELECT id_documento, tipo_documento, nombre_persona, apellido_persona, numero_identificacion, fecha_creacion, fecha_vencimiento, ruta_pdf, email_persona FROM certificadosloto")
        all_certificates = cur.fetchall()
        
        if not all_certificates:
            print("No se encontraron certificados para regenerar.")
            return

        print(f"Se encontraron {len(all_certificates)} certificados. Iniciando regeneración...")

        for cert_row in all_certificates:
            # 2. Convertir la fila de la base de datos (tupla) en un diccionario CORRECTAMENTE
            certificate_data = {
                "id_documento": cert_row,
                "tipo_documento": cert_row,
                "nombre_persona": cert_row,
                "apellido_persona": cert_row,
                "numero_identificacion": cert_row,
                "fecha_creacion": cert_row,
                "fecha_vencimiento": cert_row,
                "ruta_pdf": cert_row,
                "email_persona": cert_row
            }
            
            cert_id = certificate_data["id_documento"]
            print(f"  -> Regenerando certificado ID: {cert_id}...")

            try:
                # 3. Llamar a la función de generación de PDF
                new_pdf_filename = generate_certificate_pdf(certificate_data)

                if new_pdf_filename:
                    # 4. Actualizar la base de datos con la nueva ruta del PDF
                    cur.execute(
                        "UPDATE certificadosloto SET ruta_pdf = %s WHERE id_documento = %s",
                        (new_pdf_filename, cert_id)
                    )
                    print(f"     ...Éxito. Nuevo archivo: {new_pdf_filename}")
                else:
                    print(f"     ...ADVERTENCIA: La generación del PDF para el ID {cert_id} falló.")
            
            except Exception as e:
                print(f"     ...ERROR al procesar el certificado ID {cert_id}: {e}")
                traceback.print_exc()

        # 5. Confirmar todos los cambios en la base de datos
        conn.commit()
        cur.close()
        print("\n¡Proceso de regeneración completado!")

    except Exception as e:
        print("\n!!! ERROR CATASTRÓFICO DURANTE LA REGENERACIÓN !!!")
        traceback.print_exc()
        if conn:
            conn.rollback()
    finally:
        if conn:
            release_db_connection(conn)

if __name__ == "__main__":
    regenerate_all_pdfs()