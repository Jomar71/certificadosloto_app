from functools import wraps
from flask import session, jsonify

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_id' not in session:
            return jsonify({"message": "Acceso no autorizado."}), 401
        return f(*args, **kwargs)
    return decorated_function