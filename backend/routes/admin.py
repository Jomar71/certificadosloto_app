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
# Se elimina la importación de generate_certificate_pdf ya que no se generará el PDF al crear/actualizar

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/certificates', methods=['GET'])
@admin_required
def get_certificates():
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id_documento, tipo_documento, nombre_persona, apellido_persona, numero_identificacion, fecha_creacion, fecha_vencimiento, email_persona FROM certificadosloto ORDER BY id_documento DESC")
        
        # Mapear los resultados de la consulta a un formato de diccionario
        certificates_raw = cur.fetchall()
        certificates = []
        for row in certificates_raw:
            certificates.append({
                "id_documento": row,
                "tipo_documento": row,
                "nombre_persona": row,
                "apellido_persona": row,
                "numero_identificacion": row,
                "fecha_creacion": row.strftime('%Y-%m-%d') if row else None,
                "fecha_vencimiento": row.strftime('%Y-%m-%d') if row else None,
                "email_persona": row
            })
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
        # Se elimina 'ruta_pdf' de la selección
        cur.execute("SELECT id_documento, tipo_documento, nombre_persona, apellido_persona, numero_identificacion, fecha_creacion, fecha_vencimiento, email_persona FROM certificadosloto WHERE id_documento = %s", (cert_id,))
        cert_data = cur.fetchone()
        cur.close()
        if cert_data:
            certificate = {
                "id_documento": cert_data,
                "tipo_documento": cert_data,
                "nombre_persona": cert_data,
                "apellido_persona": cert_data,
                "numero_identificacion": cert_data,
                "fecha_creacion": cert_data.strftime('%Y-%m-%d') if cert_data else None,
                "fecha_vencimiento": cert_data.strftime('%Y-%m-%d') if cert_data else None,
                "email_persona": cert_data
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
        
        conn.commit()
        return jsonify({"message": "Certificado actualizado exitosamente."})
    except Exception as e:
        traceback.print_exc()
        if conn: conn.rollback()
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
        
        sql = """INSERT INTO certificadosloto 
                 (tipo_documento, nombre_persona, apellido_persona, numero_identificacion, fecha_creacion, fecha_vencimiento, email_persona) 
                 VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id_documento;"""
        cur.execute(sql, (
            data.get('tipo_documento'), data.get('nombre_persona'), data.get('apellido_persona'),
            data.get('numero_identificacion'), data.get('fecha_creacion'), data.get('fecha_vencimiento'),
            data.get('email_persona')
        ))
        new_cert_id = cur.fetchone() # Obtener solo el ID
        
        conn.commit()
        
        return jsonify({"message": "Certificado añadido exitosamente.", "id_documento": new_cert_id}), 201
    except Exception as e:
        traceback.print_exc()
        if conn: conn.rollback()
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
        
        if cur.rowcount > 0:
            conn.commit()
            return jsonify({"message": "Certificado eliminado exitosamente."})
        else:
            conn.rollback()
            return jsonify({"message": "Certificado no encontrado."}), 404
    except Exception as e:
        traceback.print_exc()
        if conn: conn.rollback()
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
        
        # Mapear los resultados de la consulta a un formato de diccionario
        admins_raw = cur.fetchall()
        admins = []
        for row in admins_raw:
            admins.append({
                "id_admin": row,
                "login_user": row
            })
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
        new_admin_id = cur.fetchone() # Obtener solo el ID
        conn.commit()
        
        return jsonify({"message": "Administrador añadido exitosamente.", "id_admin": new_admin_id}), 201
    except Exception as e:
        traceback.print_exc()
        if conn:
            conn.rollback()
        return jsonify({"message": f"Error interno: {e}"}), 500
    finally:
        if conn:
            release_db_connection(conn)