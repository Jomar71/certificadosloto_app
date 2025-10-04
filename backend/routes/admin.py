"""
Este módulo contiene las rutas del panel de administración para la gestión de
administradores y certificados.

Utiliza un decorador para manejar las conexiones a la base de datos y está protegido
para que solo los administradores puedan acceder.
"""

import traceback
from datetime import datetime, timedelta
from functools import wraps
from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash

from backend.db import get_db_connection, release_db_connection
from backend.auth import admin_required
from backend.pdf_generator import generate_certificate_pdf

admin_bp = Blueprint('admin', __name__)

def with_db(f):
    """
    Decorador para gestionar la conexión y el cursor de la base de datos.
    Inyecta conn y cur en las funciones de ruta y maneja el cierre.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        conn = None
        cur = None
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            # Pasa la conexión y el cursor a la función de la ruta
            return f(conn, cur, *args, **kwargs)
        except Exception as e:
            # Imprime el traceback para depuración en el servidor
            traceback.print_exc()
            # Devuelve un error genérico al cliente
            return jsonify({"message": "Error interno del servidor."}), 500
        finally:
            if cur:
                cur.close()
            if conn:
                release_db_connection(conn)
    return decorated_function

# Rutas para la gestión de administradores
@admin_bp.route('/admins', methods=['GET'])
@admin_required
@with_db
def get_admins(conn, cur):
    """Obtiene todos los administradores."""
    cur.execute("SELECT id_admin, login_user FROM administradoresloto ORDER BY id_admin DESC")
    admins = [{"id_admin": row[0], "login_user": row[1]} for row in cur.fetchall()]
    return jsonify(admins)

@admin_bp.route('/admins/<int:admin_id>', methods=['GET'])
@admin_required
@with_db
def get_single_admin(conn, cur, admin_id):
    """Obtiene un único administrador por su ID."""
    cur.execute("SELECT id_admin, login_user FROM administradoresloto WHERE id_admin = %s", (admin_id,))
    admin = cur.fetchone()
    if not admin:
        return jsonify({"message": "Administrador no encontrado"}), 404
    return jsonify({"id_admin": admin[0], "login_user": admin[1]})

@admin_bp.route('/admins', methods=['POST'])
@admin_required
@with_db
def add_admin(conn, cur):
    """Añade un nuevo administrador."""
    data = request.get_json()
    if not data or 'login_user' not in data or 'login_pass' not in data:
        return jsonify({"message": "Usuario y contraseña son requeridos"}), 400

    # Verificar si el usuario ya existe
    cur.execute("SELECT id_admin FROM administradoresloto WHERE login_user = %s", (data['login_user'],))
    if cur.fetchone():
        return jsonify({"message": "El nombre de usuario ya existe"}), 409

    hashed_password = generate_password_hash(data['login_pass'])
    sql = "INSERT INTO administradoresloto (login_user, login_pass) VALUES (%s, %s) RETURNING id_admin;"
    cur.execute(sql, (data['login_user'], hashed_password))
    new_admin_id = cur.fetchone()[0]
    conn.commit()
    return jsonify({"message": "Administrador añadido exitosamente.", "id_admin": new_admin_id}), 201

@admin_bp.route('/admins/<int:admin_id>', methods=['PUT'])
@admin_required
@with_db
def update_admin(conn, cur, admin_id):
    """Actualiza un administrador existente."""
    data = request.get_json()
    if not data:
        return jsonify({"message": "No hay datos para actualizar"}), 400

    # Verificar si el administrador existe
    cur.execute("SELECT id_admin FROM administradoresloto WHERE id_admin = %s", (admin_id,))
    if not cur.fetchone():
        return jsonify({"message": "Administrador no encontrado."}), 404

    updates = []
    params = []

    if 'login_user' in data:
        # Verificar si el nuevo login_user ya existe en otro admin
        cur.execute("SELECT id_admin FROM administradoresloto WHERE login_user = %s AND id_admin != %s", (data['login_user'], admin_id))
        if cur.fetchone():
            return jsonify({"message": "El nombre de usuario ya existe"}), 409
        updates.append("login_user = %s")
        params.append(data['login_user'])
    if 'login_pass' in data and data['login_pass']:
        hashed_password = generate_password_hash(data['login_pass'])
        updates.append("login_pass = %s")
        params.append(hashed_password)
    
    if not updates:
        return jsonify({"message": "No hay datos para actualizar"}), 400

    sql = f"UPDATE administradoresloto SET {', '.join(updates)} WHERE id_admin = %s;"
    params.append(admin_id)
    cur.execute(sql, tuple(params))
    conn.commit()

    return jsonify({"message": "Administrador actualizado exitosamente."}) if cur.rowcount > 0 else jsonify({"message": "Administrador no encontrado."}), 404

@admin_bp.route('/admins/<int:admin_id>', methods=['DELETE'])
@admin_required
@with_db
def delete_admin(conn, cur, admin_id):
    """Elimina un administrador."""
    cur.execute("DELETE FROM administradoresloto WHERE id_admin = %s;", (admin_id,))
    conn.commit()
    return jsonify({"message": "Administrador eliminado exitosamente."}) if cur.rowcount > 0 else jsonify({"message": "Administrador no encontrado."}), 404

# Rutas para la gestión de certificados
@admin_bp.route('/certificates', methods=['GET'])
@admin_required
@with_db
def get_certificates(conn, cur):
    """Obtiene todos los certificados."""
    cur.execute("SELECT id_documento, nombre_persona, apellido_persona, numero_identificacion FROM certificadosloto ORDER BY id_documento DESC")
    certificates = [{"id_documento": row[0], "nombre_persona": row[1], "apellido_persona": row[2], "numero_identificacion": row[3]} for row in cur.fetchall()]
    return jsonify(certificates)

@admin_bp.route('/certificates/<int:cert_id>', methods=['GET'])
@admin_required
@with_db
def get_single_certificate(conn, cur, cert_id):
    """Obtiene un único certificado por su ID."""
    cur.execute("SELECT * FROM certificadosloto WHERE id_documento = %s", (cert_id,))
    cert_data = cur.fetchone()
    if not cert_data:
        return jsonify({"message": "Certificado no encontrado"}), 404

    # Manejar fechas None para evitar errores en strftime
    fecha_creacion = cert_data[5].strftime('%Y-%m-%d') if cert_data[5] else None
    fecha_vencimiento = cert_data[6].strftime('%Y-%m-%d') if cert_data[6] else None

    certificate = {
        "id_documento": cert_data[0], "tipo_documento": cert_data[1], "nombre_persona": cert_data[2],
        "apellido_persona": cert_data[3], "numero_identificacion": cert_data[4],
        "fecha_creacion": fecha_creacion,
        "fecha_vencimiento": fecha_vencimiento,
        "ruta_pdf": cert_data[7], "email_persona": cert_data[8]
    }
    return jsonify(certificate)

@admin_bp.route('/certificates', methods=['POST'])
@admin_required
@with_db
def add_certificate(conn, cur):
    """Añade un nuevo certificado y genera su PDF."""
    data = request.get_json()
    required_fields = ['tipo_documento', 'nombre_persona', 'apellido_persona', 'numero_identificacion', 'fecha_creacion', 'fecha_vencimiento', 'email_persona']
    if not data or not all(field in data and data[field] for field in required_fields):
        return jsonify({"message": "Todos los campos son requeridos: tipo_documento, nombre_persona, apellido_persona, numero_identificacion, fecha_creacion, fecha_vencimiento, email_persona"}), 400

    sql = """INSERT INTO certificadosloto
             (tipo_documento, nombre_persona, apellido_persona, numero_identificacion, fecha_creacion, fecha_vencimiento, email_persona)
             VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id_documento;"""
    cur.execute(sql, (
        data['tipo_documento'], data['nombre_persona'], data['apellido_persona'],
        data['numero_identificacion'], data['fecha_creacion'], data['fecha_vencimiento'],
        data['email_persona']
    ))
    new_cert_id = cur.fetchone()[0]

    pdf_data = data.copy()
    pdf_data['id_documento'] = new_cert_id
    try:
        pdf_data['fecha_creacion'] = datetime.strptime(data['fecha_creacion'], '%Y-%m-%d')
    except ValueError:
        return jsonify({"message": "Formato de fecha inválido"}), 400

    pdf_filename = generate_certificate_pdf(pdf_data)
    if not pdf_filename:
        conn.rollback()
        return jsonify({"message": "Error al generar el PDF"}), 500

    cur.execute("UPDATE certificadosloto SET ruta_pdf = %s WHERE id_documento = %s", (pdf_filename, new_cert_id))
    conn.commit()

    return jsonify({"message": "Certificado añadido exitosamente.", "id_documento": new_cert_id}), 201

@admin_bp.route('/certificates/<int:cert_id>', methods=['PUT'])
@admin_required
@with_db
def update_certificate(conn, cur, cert_id):
    """Actualiza un certificado y regenera su PDF."""
    data = request.get_json()
    required_fields = ['tipo_documento', 'nombre_persona', 'apellido_persona', 'numero_identificacion']
    if not data or not all(field in data and data[field] for field in required_fields):
        return jsonify({"message": "Campos requeridos: tipo_documento, nombre_persona, apellido_persona, numero_identificacion"}), 400

    # Verificar si el certificado existe
    cur.execute("SELECT id_documento FROM certificadosloto WHERE id_documento = %s", (cert_id,))
    if not cur.fetchone():
        return jsonify({"message": "Certificado no encontrado"}), 404

    updates = []
    params = []
    pdf_data = {'id_documento': cert_id}

    # Campos siempre requeridos
    updates.append("tipo_documento = %s")
    params.append(data['tipo_documento'])
    pdf_data['tipo_documento'] = data['tipo_documento']

    updates.append("nombre_persona = %s")
    params.append(data['nombre_persona'])
    pdf_data['nombre_persona'] = data['nombre_persona']

    updates.append("apellido_persona = %s")
    params.append(data['apellido_persona'])
    pdf_data['apellido_persona'] = data['apellido_persona']

    updates.append("numero_identificacion = %s")
    params.append(data['numero_identificacion'])
    pdf_data['numero_identificacion'] = data['numero_identificacion']

    # Fechas opcionales
    if 'fecha_creacion' in data and data['fecha_creacion']:
        try:
            fecha_creacion = datetime.strptime(data['fecha_creacion'], '%Y-%m-%d')
            updates.append("fecha_creacion = %s")
            params.append(fecha_creacion)
            pdf_data['fecha_creacion'] = fecha_creacion
        except ValueError:
            return jsonify({"message": "Formato de fecha de creación inválido"}), 400
    else:
        # Usar fecha existente para PDF
        cur.execute("SELECT fecha_creacion FROM certificadosloto WHERE id_documento = %s", (cert_id,))
        existing = cur.fetchone()
        pdf_data['fecha_creacion'] = existing[0] if existing and existing[0] else datetime.now()

    if 'fecha_vencimiento' in data and data['fecha_vencimiento']:
        try:
            fecha_vencimiento = datetime.strptime(data['fecha_vencimiento'], '%Y-%m-%d')
            updates.append("fecha_vencimiento = %s")
            params.append(fecha_vencimiento)
            pdf_data['fecha_vencimiento'] = fecha_vencimiento
        except ValueError:
            return jsonify({"message": "Formato de fecha de vencimiento inválido"}), 400
    else:
        # Usar fecha existente para PDF
        cur.execute("SELECT fecha_vencimiento FROM certificadosloto WHERE id_documento = %s", (cert_id,))
        existing = cur.fetchone()
        pdf_data['fecha_vencimiento'] = existing[0] if existing and existing[0] else datetime.now() + timedelta(days=365)

    # Email opcional
    if 'email_persona' in data:
        updates.append("email_persona = %s")
        params.append(data['email_persona'])
        pdf_data['email_persona'] = data['email_persona']
    else:
        # Usar email existente para PDF
        cur.execute("SELECT email_persona FROM certificadosloto WHERE id_documento = %s", (cert_id,))
        existing = cur.fetchone()
        pdf_data['email_persona'] = existing[0] if existing and existing[0] else ''

    if updates:
        sql = f"UPDATE certificadosloto SET {', '.join(updates)} WHERE id_documento = %s;"
        params.append(cert_id)
        cur.execute(sql, tuple(params))

    pdf_filename = generate_certificate_pdf(pdf_data)
    if not pdf_filename:
        conn.rollback()
        return jsonify({"message": "Error al regenerar el PDF"}), 500

    cur.execute("UPDATE certificadosloto SET ruta_pdf = %s WHERE id_documento = %s", (pdf_filename, cert_id))
    conn.commit()

    return jsonify({"message": "Certificado actualizado y PDF regenerado exitosamente."})

@admin_bp.route('/certificates/<int:cert_id>', methods=['DELETE'])
@admin_required
@with_db
def delete_certificate(conn, cur, cert_id):
    """Elimina un certificado."""
    cur.execute("DELETE FROM certificadosloto WHERE id_documento = %s;", (cert_id,))
    if cur.rowcount > 0:
        conn.commit()
        return jsonify({"message": "Certificado eliminado exitosamente."})
    else:
        return jsonify({"message": "Certificado no encontrado."}), 404