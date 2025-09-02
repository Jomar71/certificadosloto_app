# ===================================================================================
# Contenido FINAL Y COMPLETO para: backend/routes/certificate.py
# Se restaura la lógica completa de la función de descarga.
# ===================================================================================

from flask import Blueprint, request, jsonify, current_app, send_from_directory
import os
import traceback

# Lógica de importación universal
try:
    from ..db import get_db_connection, release_db_connection
except ImportError:
    from db import get_db_connection, release_db_connection

certificate_bp = Blueprint('certificate', __name__)

@certificate_bp.route('/certificates/search', methods=['GET'])
def search_certificate():
    # ... (esta función de búsqueda ya está bien, la dejamos como está)
    print("--- Recibida petición en /api/certificates/search ---")
    cedula = request.args.get('cedula', '').strip()
    if not cedula:
        return jsonify({"message": "El parámetro 'cedula' es requerido."}), 400
    
    conn = None
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({"message": "Error crítico: No se pudo conectar a la base de datos."}), 500
        cur = conn.cursor()
        cur.execute("SELECT * FROM certificadosloto WHERE numero_identificacion = %s", (cedula,))
        cert_data = cur.fetchone()
        cur.close()
        if cert_data:
            certificate = {
                "id_documento": cert_data[0], "tipo_documento": cert_data[1], "nombre_persona": cert_data[2],
                "apellido_persona": cert_data[3], "numero_identificacion": cert_data[4],
                "fecha_creacion": cert_data[5].strftime('%Y-%m-%d') if cert_data[5] else None,
                "fecha_vencimiento": cert_data[6].strftime('%Y-%m-%d') if cert_data[6] else None,
                "ruta_pdf": cert_data[7], "email_persona": cert_data[8]
            }
            return jsonify(certificate)
        else:
            return jsonify({"message": "No se encontró ningún certificado con la cédula proporcionada."}), 404
    except Exception as e:
        traceback.print_exc()
        return jsonify({"message": "Error interno del servidor."}), 500
    finally:
        if conn:
            release_db_connection(conn)

# --- ¡¡AQUÍ ESTÁ LA FUNCIÓN CORREGIDA!! ---
@certificate_bp.route('/certificates/<int:cert_id>/download', methods=['GET'])
def download_certificate(cert_id):
    """
    Busca el nombre del archivo PDF en la base de datos y lo envía para su descarga.
    """
    print(f"--- Recibida petición para descargar PDF del certificado ID: {cert_id} ---")
    conn = None
    try:
        conn = get_db_connection()
        if not conn:
            return "Error de conexión con la base de datos", 500

        cur = conn.cursor()
        cur.execute("SELECT ruta_pdf, nombre_persona, apellido_persona FROM certificadosloto WHERE id_documento = %s", (cert_id,))
        result = cur.fetchone()
        cur.close()

        if result and result[0]: # Si se encontró el registro Y la columna ruta_pdf no está vacía
            pdf_filename = result[0]
            person_name = f"{result[1]} {result[2]}"
            
            # Directorio donde se guardan los PDFs generados
            pdf_directory = os.path.join(current_app.root_path, 'certificates_generated')
            
            print(f" -> Intentando enviar el archivo: {pdf_filename} desde {pdf_directory}")

            # Flask se encarga de enviar el archivo
            return send_from_directory(
                directory=pdf_directory,
                path=pdf_filename,
                as_attachment=True, # Esto le dice al navegador que lo descargue en lugar de mostrarlo
                download_name=f"Certificado-{person_name}.pdf" # Nombre amigable para el usuario
            )
        else:
            print(" -> FALLO: No se encontró el registro o la ruta del PDF es nula.")
            # Es importante devolver una respuesta válida, incluso si es un error
            return "No se encontró el archivo del certificado en la base de datos.", 404

    except Exception as e:
        print(f"!!! ERROR CATASTRÓFICO en download_certificate: {e} !!!")
        traceback.print_exc()
        return "Error interno del servidor al procesar la descarga.", 500
    finally:
        if conn:
            release_db_connection(conn)
            print("--- Conexión a BD (descarga) liberada ---")