#!/usr/bin/env python3
"""
Script para regenerar todos los PDFs de certificados con los cambios en pdf_generator.py
"""

import os
import sys
from datetime import datetime

# Añadir el directorio backend al path para importar módulos
sys.path.insert(0, os.path.dirname(__file__))

from db import get_db_connection, release_db_connection
from pdf_generator import generate_certificate_pdf

def regenerate_all_pdfs():
    conn = None
    cur = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # Obtener todos los certificados
        cur.execute("SELECT id_documento, tipo_documento, nombre_persona, apellido_persona, numero_identificacion, fecha_creacion, fecha_vencimiento, email_persona FROM certificadosloto")
        certificates = cur.fetchall()

        print(f"Encontrados {len(certificates)} certificados para regenerar.")

        for cert in certificates:
            cert_data = {
                'id_documento': cert[0],
                'tipo_documento': cert[1],
                'nombre_persona': cert[2],
                'apellido_persona': cert[3],
                'numero_identificacion': cert[4],
                'fecha_creacion': cert[5],
                'fecha_vencimiento': cert[6],
                'email_persona': cert[7]
            }

            print(f"Regenerando PDF para certificado ID {cert[0]}...")

            pdf_filename = generate_certificate_pdf(cert_data)
            if pdf_filename:
                cur.execute("UPDATE certificadosloto SET ruta_pdf = %s WHERE id_documento = %s", (pdf_filename, cert[0]))
                print(f"PDF actualizado para ID {cert[0]}: {pdf_filename}")
            else:
                print(f"Error al generar PDF para ID {cert[0]}")

        conn.commit()
        print("Todos los PDFs han sido regenerados exitosamente.")

    except Exception as e:
        print(f"Error durante la regeneración: {e}")
        if conn:
            conn.rollback()
    finally:
        if cur:
            cur.close()
        if conn:
            release_db_connection(conn)

if __name__ == "__main__":
    regenerate_all_pdfs()
