# ===================================================================================
# ARCHIVO FINAL, COMPLETO Y CORREGIDO PARA: backend/routes/certificate.py
# ===================================================================================

from flask import Blueprint, request, jsonify, current_app, send_file
import os
import traceback
from datetime import datetime # Importar datetime para formatear fechas
from io import BytesIO # Para manejar el PDF en memoria

# Usamos una importación absoluta que funcionará con app.py en la raíz
from backend.db import get_db_connection, release_db_connection
from backend.pdf_generator import generate_certificate_pdf # Importar el generador de PDF

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
        # Se elimina 'ruta_pdf' de la selección
        cur.execute("SELECT id_documento, tipo_documento, nombre_persona, apellido_persona, numero_identificacion, fecha_creacion, fecha_vencimiento, email_persona FROM certificadosloto WHERE numero_identificacion = %s", (cedula,))
        cert_data = cur.fetchone()
        cur.close()
        
        if cert_data:
            certificate = {
                "id_documento": cert_data, "tipo_documento": cert_data, "nombre_persona": cert_data,
                "apellido_persona": cert_data, "numero_identificacion": cert_data,
                "fecha_creacion": cert_data.strftime('%Y-%m-%d') if cert_data else None,
                "fecha_vencimiento": cert_data.strftime('%Y-%m-%d') if cert_data else None,
                "email_persona": cert_data
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
    Genera el PDF del certificado dinámicamente y lo envía para su descarga.
    """
    conn = None
    try:
        conn = get_db_connection()
        if not conn:
            return "Error de conexión con la base de datos", 500

        cur = conn.cursor()
        # Seleccionar todos los datos necesarios para generar el PDF
        cur.execute("SELECT id_documento, tipo_documento, nombre_persona, apellido_persona, numero_identificacion, fecha_creacion, fecha_vencimiento, email_persona FROM certificadosloto WHERE id_documento = %s", (cert_id,))
        cert_data_raw = cur.fetchone()
        cur.close()

        if not cert_data_raw:
            return "No se encontró el certificado.", 404

        # Reconstruir el diccionario de datos del certificado
        cert_data = {
            "id_documento": cert_data_raw,
            "tipo_documento": cert_data_raw,
            "nombre_persona": cert_data_raw,
            "apellido_persona": cert_data_raw,
            "numero_identificacion": cert_data_raw,
            "fecha_creacion": cert_data_raw, # Ya es un objeto datetime
            "fecha_vencimiento": cert_data_raw, # Ya es un objeto datetime
            "email_persona": cert_data_raw
        }

        # Generar el PDF en memoria
        pdf_buffer = BytesIO()
        filename = generate_certificate_pdf(cert_data, output_buffer=pdf_buffer)
        
        if not filename:
            return "Error al generar el PDF del certificado.", 500

        pdf_buffer.seek(0) # Volver al inicio del buffer

        return send_file(
            pdf_buffer,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=filename
        )

    except Exception:
        traceback.print_exc()
        return "Error interno del servidor al procesar la descarga.", 500
    finally:
        if conn:
            release_db_connection(conn)

@certificate_bp.route('/<int:cert_id>/send_email', methods=['POST'])
def send_certificate_email(cert_id):
    """
    Simula el envío de un certificado por correo electrónico.
    """
    data = request.get_json()
    email = data.get('email')

    if not email:
        return jsonify({"message": "La dirección de correo es requerida."}), 400

    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        # Seleccionar todos los datos necesarios para generar el PDF para el correo
        cur.execute("SELECT id_documento, tipo_documento, nombre_persona, apellido_persona, numero_identificacion, fecha_creacion, fecha_vencimiento, email_persona FROM certificadosloto WHERE id_documento = %s", (cert_id,))
        cert_data_raw = cur.fetchone()
        cur.close()

        if not cert_data_raw:
            return jsonify({"message": "No se encontró el certificado para enviar."}), 404

        # Reconstruir el diccionario de datos del certificado
        cert_data = {
            "id_documento": cert_data_raw,
            "tipo_documento": cert_data_raw,
            "nombre_persona": cert_data_raw,
            "apellido_persona": cert_data_raw,
            "numero_identificacion": cert_data_raw,
            "fecha_creacion": cert_data_raw,
            "fecha_vencimiento": cert_data_raw,
            "email_persona": cert_data_raw
        }

        # Generar el PDF en memoria para adjuntar al correo
        pdf_buffer = BytesIO()
        pdf_filename = generate_certificate_pdf(cert_data, output_buffer=pdf_buffer)

        if not pdf_filename:
            raise Exception("La función generate_certificate_pdf devolvió None.")
            
        # --- SIMULACIÓN DE ENVÍO DE CORREO ---
        # En una implementación real, aquí iría la lógica para enviar el correo
        # con el archivo adjunto (usando Flask-Mail, smtplib, etc.).
        print("="*50)
        print(f"SIMULACIÓN: Enviando correo a: {email}")
        print(f"Asunto: Su certificado de {cert_data['nombre_persona']}")
        print(f"Adjunto: {pdf_filename}")
        print(f"ID de Certificado: {cert_id}")
        print("="*50)
        
        return jsonify({"message": f"El certificado ha sido enviado exitosamente a {email}."})
    except Exception as e:
        traceback.print_exc()
        return jsonify({"message": "Error interno del servidor al procesar el envío."}), 500
    finally:
        if conn:
            release_db_connection(conn)