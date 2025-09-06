# ===================================================================================
# ARCHIVO FINAL, COMPLETO Y CORREGIDO PARA: backend/routes/certificate.py
# ===================================================================================

from flask import Blueprint, request, jsonify, current_app, send_from_directory
import os
import traceback

# Usamos una importación absoluta que funcionará con app.py en la raíz
from backend.db import get_db_connection, release_db_connection

certificate_bp = Blueprint('certificate', __name__)

@certificate_bp.route('/certificates/search', methods=['GET'])
def search_certificate():
    """
    Busca un certificado por número de cédula. Versión a prueba de fallos.
    """
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
    except Exception:
        # Si algo falla, lo imprimirá en la terminal y devolverá un error claro
        traceback.print_exc()
        return jsonify({"message": "Error interno del servidor al buscar el certificado."}), 500
    finally:
        if conn:
            release_db_connection(conn)


@certificate_bp.route('/certificates/<int:cert_id>/download', methods=['GET'])
def download_certificate(cert_id):
    """
    Busca el nombre del archivo PDF en la base de datos y lo envía para su descarga.
    """
    conn = None
    try:
        conn = get_db_connection()
        if not conn:
            return "Error de conexión con la base de datos", 500

        cur = conn.cursor()
        cur.execute("SELECT ruta_pdf FROM certificadosloto WHERE id_documento = %s", (cert_id,))
        result = cur.fetchone()
        cur.close()

        if result and result[0]:
            pdf_filename = result[0]
            # Usamos una ruta absoluta para máxima fiabilidad
            backend_folder = os.path.dirname(os.path.abspath(__file__))
            pdf_directory = os.path.join(backend_folder, '..', 'certificates_generated')
            
            if not os.path.exists(os.path.join(pdf_directory, pdf_filename)):
                return "El archivo PDF no se encuentra en el servidor, necesita ser generado por un administrador.", 404

            return send_from_directory(
                directory=pdf_directory,
                path=pdf_filename,
                as_attachment=True
            )
        else:
            return "No se encontró el registro o la ruta del PDF es nula.", 404
    except Exception:
        traceback.print_exc()
        return "Error interno del servidor al procesar la descarga.", 500
    finally:
        if conn:
            release_db_connection(conn)