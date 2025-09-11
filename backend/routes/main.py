# ===================================================================================
# ARCHIVO COMPLETO Y CORREGIDO PARA: backend/routes/main.py
# ===================================================================================
from flask import Blueprint, request, jsonify, session
from werkzeug.security import check_password_hash
import traceback

# ¡IMPORTACIONES CORREGIDAS! Ahora buscan desde la raíz del proyecto.
from backend.db import get_db_connection, release_db_connection
from backend.auth import admin_required

main_bp = Blueprint('main', __name__)

@main_bp.route('/login_admin', methods=['POST'])
def login_admin():
    data = request.get_json()
    if not data or 'login_user' not in data or 'login_pass' not in data:
        return jsonify({"message": "Usuario y contraseña son requeridos"}), 400
    
    conn = None
    try:
        conn = get_db_connection()
        if not conn: return jsonify({"message": "Error de conexión con la base de datos"}), 500
        
        cur = conn.cursor()
        cur.execute("SELECT admin_id, login_user, login_pass FROM administradores WHERE login_user = %s", (data['login_user'],))
        admin = cur.fetchone()
        cur.close()

        if admin and check_password_hash(admin[2], data['login_pass']):
            session.permanent = True
            session['admin_id'] = admin[0]
            session['login_user'] = admin[1]
            return jsonify({"message": f"Bienvenido {admin[1]}"}), 200
        else:
            return jsonify({"message": "Credenciales inválidas"}), 401
    except Exception:
        traceback.print_exc()
        return jsonify({"message": "Error interno del servidor"}), 500
    finally:
        if conn: release_db_connection(conn)

@main_bp.route('/logout_admin', methods=['POST'])
def logout_admin():
    session.clear()
    return jsonify({"message": "Sesión cerrada exitosamente"}), 200

@main_bp.route('/is_admin', methods=['GET'])
@admin_required
def is_admin():
    if 'admin_id' in session:
        return jsonify({"is_admin": True, "login_user": session.get('login_user')})
    else:
        # Este caso no debería ocurrir gracias a @admin_required, pero es una buena práctica
        return jsonify({"is_admin": False})