# ===================================================================================
# ARCHIVO COMPLETO Y ESTABLE PARA: backend/routes/admin.py
# ===================================================================================

from flask import Blueprint, request, jsonify
from datetime import datetime
import traceback

# Usamos importaciones directas
from db import get_db_connection, release_db_connection
from auth import admin_required
from pdf_generator import generate_certificate_pdf

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/admin/certificates', methods=['GET'])
@admin_required
def get_certificates():
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id_documento, nombre_persona, apellido_persona, numero_identificacion FROM certificadosloto ORDER BY id_documento DESC")
        certificates = [{"id_documento": row[0], "nombre_persona": row[1], "apellido_persona": row[2], "numero_identificacion": row[3]} for row in cur.fetchall()]
        cur.close()
        return jsonify(certificates)
    except Exception:
        traceback.print_exc()
        return jsonify({"message": "Error al cargar certificados"}), 500
    finally:
        if conn:
            release_db_connection(conn)

@admin_bp.route('/admin/certificates/<int:cert_id>', methods=['GET'])
@admin_required
def get_single_certificate(cert_id):
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM certificadosloto WHERE id_documento = %s", (cert_id,))
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
            return jsonify({"message": "Certificado no encontrado"}), 404
    except Exception:
        traceback.print_exc()
        return jsonify({"message": "Error interno"}), 500
    finally:
        if conn:
            release_db_connection(conn)

@admin_bp.route('/admin/certificates/<int:cert_id>', methods=['PUT'])
@admin_required
def update_certificate(cert_id):
    data = request.get_json()
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        sql = """UPDATE certificadosloto SET 
                 tipo_documento = %s, nombre_persona = %s, apellido_persona = %s, 
                 numero_identificacion = %s, fecha_creacion = %s, fecha_vencimiento = %s, email_persona = %s
                 WHERE id_documento = %s;"""
        cur.execute(sql, (
            data.get('tipo_documento'), data.get('nombre_persona'), data.get('apellido_persona'),
            data.get('numero_identificacion'), data.get('fecha_creacion'), data.get('fecha_vencimiento'),
            data.get('email_persona'), cert_id
        ))

        pdf_data = data.copy()
        pdf_data['id_documento'] = cert_id
        pdf_data['fecha_creacion'] = datetime.strptime(data['fecha_creacion'], '%Y-%m-%d')
        
        pdf_filename = generate_certificate_pdf(pdf_data)

        if pdf_filename:
            cur.execute("UPDATE certificadosloto SET ruta_pdf = %s WHERE id_documento = %s", (pdf_filename, cert_id))
        else:
            conn.rollback()
            raise Exception("La función generate_certificate_pdf devolvió None.")
        
        conn.commit()
        return jsonify({"message": "Certificado actualizado y PDF regenerado exitosamente."})
    except Exception as e:
        if conn: conn.rollback()
        traceback.print_exc()
        return jsonify({"message": f"Error interno: {e}"}), 500
    finally:
        if conn:
            release_db_connection(conn)

# (Aquí se añadiría la ruta POST para crear certificados, una vez que esto funcione)