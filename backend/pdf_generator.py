# ===================================================================================
# ARCHIVO FINAL Y COMPLETO PARA: backend/pdf_generator.py
# A PRUEBA DE FALLOS: Si una fuente no carga, usa Helvetica en su lugar.
# ===================================================================================

import os
import traceback
from datetime import datetime
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

meses_es = {"January":"Enero", "February":"Febrero", "March":"Marzo", "April":"Abril", "May":"Mayo", "June":"Junio", "July":"Julio", "August":"Agosto", "September":"Septiembre", "October":"Octubre", "November":"Noviembre", "December":"Diciembre"}

def generate_certificate_pdf(certificate_data):
    try:
        backend_folder = os.path.dirname(os.path.abspath(__file__))
        filename = f"certificado_{certificate_data.get('numero_identificacion', 'sincodigo')}_{certificate_data.get('id_documento', 'sinid')}.pdf"
        output_dir = os.path.join(backend_folder, 'certificates_generated')
        os.makedirs(output_dir, exist_ok=True)
        filepath = os.path.join(output_dir, filename)

        c = canvas.Canvas(filepath, pagesize=landscape(letter))
        width, height = landscape(letter)

        # --- REGISTRO DE FUENTES (CON MÉTODO A PRUEBA DE FALLOS) ---
        nombre_font_name = 'Helvetica-Bold' # Fuente por defecto
        texto_font_name = 'Helvetica'      # Fuente por defecto
        try:
            font_greatvibes_path = os.path.join(backend_folder, 'fonts', 'GreatVibes-Regular.ttf')
            pdfmetrics.registerFont(TTFont('GreatVibes', font_greatvibes_path))
            nombre_font_name = 'GreatVibes' # Si tiene éxito, la usamos
        except: print("ADVERTENCIA: No se pudo registrar GreatVibes-Regular.ttf.")
        
        try:
            font_garet_path = os.path.join(backend_folder, 'fonts', 'Garet-Book.otf')
            pdfmetrics.registerFont(TTFont('Garet-Book', font_garet_path))
            texto_font_name = 'Garet-Book' # Si tiene éxito, la usamos
        except: print("ADVERTENCIA: No se pudo registrar Garet-Book.otf.")
        
        # --- DIBUJAR LA PLANTILLA ---
        template_filename = 'plantilla.jpg' 
        template_path = os.path.join(backend_folder, 'static', template_filename)

        if os.path.exists(template_path):
            c.drawImage(template_path, 0, 0, width=width, height=height, preserveAspectRatio=True, anchor='c')

        # ==========================================================================
        # === ZONA DE PERSONALIZACIÓN ===
        # ==========================================================================
        nombre = certificate_data.get('nombre_persona', '')
        apellido = certificate_data.get('apellido_persona', '')
        full_name = f"{nombre} {apellido}".strip().title()
        full_name_font = nombre_font_name # Usa la fuente que se haya podido cargar
        full_name_size = 55
        full_name_color = '#873233'
        full_name_x = width / 1.9
        full_name_y = 267

        id_text = f"No. {certificate_data.get('numero_identificacion', 'N/A')}"
        id_font = texto_font_name # Usa la fuente que se haya podido cargar
        id_size = 14
        id_color = '#873233'
        id_x = width / 1.7
        id_y = 240

        # Fechas
        fecha_creacion = certificate_data.get('fecha_creacion', '')
        fecha_vencimiento = certificate_data.get('fecha_vencimiento', '')
        if fecha_creacion:
            if isinstance(fecha_creacion, str):
                dt_creacion = datetime.fromisoformat(fecha_creacion)
            else:
                dt_creacion = fecha_creacion
            mes_creacion = meses_es.get(dt_creacion.strftime('%B'), dt_creacion.strftime('%B'))
            fecha_creacion_formatted = f"{dt_creacion.day:02d} de {mes_creacion} {dt_creacion.year}"
        else:
            fecha_creacion_formatted = 'N/A'
        if fecha_vencimiento:
            if isinstance(fecha_vencimiento, str):
                dt_vencimiento = datetime.fromisoformat(fecha_vencimiento)
            else:
                dt_vencimiento = fecha_vencimiento
            mes_vencimiento = meses_es.get(dt_vencimiento.strftime('%B'), dt_vencimiento.strftime('%B'))
            fecha_vencimiento_formatted = f"{dt_vencimiento.day:02d} de {mes_vencimiento} {dt_vencimiento.year}"
        else:
            fecha_vencimiento_formatted = 'N/A'

        fecha_creacion_text = f"Dado el: {fecha_creacion_formatted}"
        fecha_creacion_font = texto_font_name
        fecha_creacion_size = 12
        fecha_creacion_color = '#873233'
        fecha_creacion_x = width / 3.6   # Posición ajustable
        fecha_creacion_y = 190  # Posición ajustable

        fecha_vencimiento_text = f"Vence el: {fecha_vencimiento_formatted}"
        fecha_vencimiento_font = texto_font_name
        fecha_vencimiento_size = 12
        fecha_vencimiento_color = '#873233'
        fecha_vencimiento_x = width / 1.9  # Posición ajustable
        fecha_vencimiento_y = 190   # Posición ajustable

        # ==========================================================================

        c.setFont(full_name_font, full_name_size)
        c.setFillColor(HexColor(full_name_color))
        c.drawCentredString(full_name_x, full_name_y, full_name)

        c.setFont(id_font, id_size)
        c.setFillColor(HexColor(id_color))
        c.drawCentredString(id_x, id_y, id_text)

        c.setFont(fecha_creacion_font, fecha_creacion_size)
        c.setFillColor(HexColor(fecha_creacion_color))
        c.drawString(fecha_creacion_x, fecha_creacion_y, fecha_creacion_text)

        c.setFont(fecha_vencimiento_font, fecha_vencimiento_size)
        c.setFillColor(HexColor(fecha_vencimiento_color))
        c.drawString(fecha_vencimiento_x, fecha_vencimiento_y, fecha_vencimiento_text)
        
        c.save()
        return filename
    except Exception:
        print("\n!!! ERROR CATASTRÓFICO DENTRO DE PDF_GENERATOR !!!")
        traceback.print_exc()
        return None