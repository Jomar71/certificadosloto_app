# ===================================================================================
# ARCHIVO COMPLETO Y FUNCIONAL PARA: backend/routes/admin.py
# Se rellenan TODAS las funciones necesarias para el panel.
# ===================================================================================

from flask import Blueprint, request, jsonify
from datetime import datetime
import traceback
from werkzeug.security import generate_password_hash

from backend.db import get_db_connection, release_db_connection
from backend.auth import admin_required
from backend.pdf_generator import generate_certificate_pdf

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/certificates', methods=['GET'])
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
    except Exception as e:
        traceback.print_exc()
        return jsonify({"message": "Error al cargar certificados"}), 500
    finally:
        if conn: release_db_connection(conn)

# --- ¡FUNCIÓN RESTAURADA! ---
@admin_bp.route('/certificates/<int:cert_id>', methods=['GET'])
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
    except Exception as e:
        traceback.print_exc()
        return jsonify({"message": "Error interno"}), 500
    finally:
        if conn: release_db_connection(conn)

# --- ¡FUNCIÓN RESTAURADA! ---
@admin_bp.route('/certificates/<int:cert_id>', methods=['PUT'])
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
        # Convertir fechas de string a objeto datetime para el generador de PDF
        if data.get('fecha_creacion'):
            pdf_data['fecha_creacion'] = datetime.strptime(data['fecha_creacion'], '%Y-%m-%d')
        if data.get('fecha_vencimiento'):
            pdf_data['fecha_vencimiento'] = datetime.strptime(data['fecha_vencimiento'], '%Y-%m-%d')
        
        pdf_filename = generate_certificate_pdf(pdf_data)

        if pdf_filename:
            cur.execute("UPDATE certificadosloto SET ruta_pdf = %s WHERE id_documento = %s", (pdf_filename, cert_id))
        else:
            raise Exception("La función generate_certificate_pdf devolvió None.")
        
        conn.commit()
        return jsonify({"message": "Certificado actualizado y PDF regenerado exitosamente."})
    except Exception as e:
        traceback.print_exc()
        return jsonify({"message": f"Error interno: {e}"}), 500
    finally:
        if conn: release_db_connection(conn)
@admin_bp.route('/certificates', methods=['POST'])
@admin_required
def add_certificate():
    data = request.get_json()
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Inserta los datos iniciales sin la ruta del PDF
        sql = """INSERT INTO certificadosloto 
                 (tipo_documento, nombre_persona, apellido_persona, numero_identificacion, fecha_creacion, fecha_vencimiento, email_persona) 
                 VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id_documento;"""
        cur.execute(sql, (
            data.get('tipo_documento'), data.get('nombre_persona'), data.get('apellido_persona'),
            data.get('numero_identificacion'), data.get('fecha_creacion'), data.get('fecha_vencimiento'),
            data.get('email_persona')
        ))
        new_cert_id = cur.fetchone()[0]

        # Prepara datos para generar el PDF
        pdf_data = data.copy()
        pdf_data['id_documento'] = new_cert_id
        # Convertir fechas de string a objeto datetime para el generador de PDF
        if data.get('fecha_creacion'):
            pdf_data['fecha_creacion'] = datetime.strptime(data['fecha_creacion'], '%Y-%m-%d')
        if data.get('fecha_vencimiento'):
            pdf_data['fecha_vencimiento'] = datetime.strptime(data['fecha_vencimiento'], '%Y-%m-%d')

        # Genera el PDF
        pdf_filename = generate_certificate_pdf(pdf_data)

        if pdf_filename:
            # Actualiza el registro con la ruta del PDF
            cur.execute("UPDATE certificadosloto SET ruta_pdf = %s WHERE id_documento = %s", (pdf_filename, new_cert_id))
        else:
            # Si la generación del PDF falla, revierte toda la transacción
            raise Exception("La función generate_certificate_pdf devolvió None.")

        # ¡¡ESTE ES EL PASO CRUCIAL QUE FALTABA!!
        
        conn.commit()
        
        return jsonify({"message": "Certificado añadido exitosamente.", "id_documento": new_cert_id}), 201
    except Exception as e:
        traceback.print_exc()
        return jsonify({"message": f"Error interno: {e}"}), 500
    finally:
        if conn: release_db_connection(conn)

@admin_bp.route('/certificates/<int:cert_id>', methods=['DELETE'])
@admin_required
def delete_certificate(cert_id):
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM certificadosloto WHERE id_documento = %s;", (cert_id,))
        
        # ¡¡CONFIRMAR LA TRANSACCIÓN!!
        
        if cur.rowcount > 0:
            conn.commit()
            return jsonify({"message": "Certificado eliminado exitosamente."})
        else:
            return jsonify({"message": "Certificado no encontrado."}), 404
    except Exception as e:
        traceback.print_exc()
        return jsonify({"message": f"Error interno: {e}"}), 500
    finally:
        if conn: release_db_connection(conn)

# --- GESTIÓN DE ADMINISTRADORES ---

@admin_bp.route('/admins', methods=['GET'])
@admin_required
def get_admins():
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id_admin, login_user FROM administradoresloto ORDER BY login_user")
        admins = [{"id_admin": row[0], "login_user": row[1]} for row in cur.fetchall()]
        cur.close()
        return jsonify(admins)
    except Exception as e:
        traceback.print_exc()
        return jsonify({"message": "Error al cargar administradores"}), 500
    finally:
        if conn: release_db_connection(conn)

@admin_bp.route('/admins', methods=['POST'])
@admin_required
def add_admin():
    data = request.get_json()
    login_user = data.get('login_user')
    login_pass = data.get('login_pass')

    if not login_user or not login_pass:
        return jsonify({"message": "Usuario y contraseña son requeridos."}), 400

    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Se hashea la contraseña antes de guardarla en la base de datos
        hashed_pass = generate_password_hash(login_pass)
        sql = "INSERT INTO administradoresloto (login_user, login_pass) VALUES (%s, %s) RETURNING id_admin;"
        cur.execute(sql, (login_user, hashed_pass))
        new_admin_id = cur.fetchone()[0]
        conn.commit()
        
        return jsonify({"message": "Administrador añadido exitosamente.", "id_admin": new_admin_id}), 201
    except Exception as e:
        traceback.print_exc()
        if conn: conn.rollback()
        return jsonify({"message": f"Error interno: {e}"}), 500
    finally:
        if conn: release_db_connection(conn)