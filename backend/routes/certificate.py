# ===================================================================================
# ARCHIVO FINAL, COMPLETO Y CORREGIDO PARA: backend/routes/certificate.py
# ===================================================================================

from flask import Blueprint, request, jsonify, current_app, send_from_directory
import os
import traceback

# Usamos una importación absoluta que funcionará con app.py en la raíz
from backend.db import get_db_connection, release_db_connection

certificate_bp = Blueprint('certificate', __name__)

@certificate_bp.route('/search', methods=['GET'])
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


@certificate_bp.route('/<int:cert_id>/download', methods=['GET'])
def download_certificate(cert_id):
    """
    Busca el nombre del archivo PDF en la base de datos y lo envía para su descarga.
    Si el PDF no existe, lo regenera automáticamente.
    """
    conn = None
    cur = None
    try:
        conn = get_db_connection()
        if not conn:
            return "Error de conexión con la base de datos", 500

        cur = conn.cursor()
        cur.execute("SELECT ruta_pdf FROM certificadosloto WHERE id_documento = %s", (cert_id,))
        result = cur.fetchone()

        if not result or not result[0]:
            return "No se encontró el registro o la ruta del PDF es nula.", 404

        pdf_filename = result[0]
        # Usamos una ruta absoluta para máxima fiabilidad
        backend_folder = os.path.dirname(os.path.abspath(__file__))
        pdf_directory = os.path.join(backend_folder, '..', 'certificates_generated')
        pdf_filepath = os.path.join(pdf_directory, pdf_filename)

        if not os.path.exists(pdf_filepath):
            # Regenerar el PDF si no existe
            cur.execute("SELECT tipo_documento, nombre_persona, apellido_persona, numero_identificacion, fecha_creacion, fecha_vencimiento, email_persona FROM certificadosloto WHERE id_documento = %s", (cert_id,))
            cert_data = cur.fetchone()
            if not cert_data:
                return "Certificado no encontrado.", 404

            cert_dict = {
                'id_documento': cert_id,
                'tipo_documento': cert_data[0],
                'nombre_persona': cert_data[1],
                'apellido_persona': cert_data[2],
                'numero_identificacion': cert_data[3],
                'fecha_creacion': cert_data[4],
                'fecha_vencimiento': cert_data[5],
                'email_persona': cert_data[6]
            }

            from backend.pdf_generator import generate_certificate_pdf
            new_pdf_filename = generate_certificate_pdf(cert_dict)
            if not new_pdf_filename:
                return "Error al regenerar el PDF.", 500

            # Actualizar la ruta en la base de datos si cambió (aunque no debería)
            if new_pdf_filename != pdf_filename:
                cur.execute("UPDATE certificadosloto SET ruta_pdf = %s WHERE id_documento = %s", (new_pdf_filename, cert_id))
                conn.commit()

            pdf_filename = new_pdf_filename

        return send_from_directory(
            directory=pdf_directory,
            path=pdf_filename,
            as_attachment=True
        )
    except Exception:
        traceback.print_exc()
        return "Error interno del servidor al procesar la descarga.", 500
    finally:
        if cur:
            cur.close()
        if conn:
            release_db_connection(conn)
