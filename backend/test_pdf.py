# Contenido para: backend/test_pdf.py

import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

def test_generate():
    print("--- Iniciando prueba de generación de PDF aislada ---")
    try:
        backend_folder = os.path.dirname(os.path.abspath(__file__))
        
        filepath = os.path.join(backend_folder, 'TEST_CERTIFICATE.pdf')
        c = canvas.Canvas(filepath, pagesize=landscape(letter))
        width, height = landscape(letter)

        # --- Prueba de Fuentes ---
        try:
            font_greatvibes_path = os.path.join(backend_folder, 'fonts', 'GreatVibes-Regular.ttf')
            pdfmetrics.registerFont(TTFont('GreatVibes', font_greatvibes_path))
            nombre_font_name = 'GreatVibes'
            print(" -> Fuente GreatVibes OK")
        except Exception as e:
            print(f" -> ERROR al cargar GreatVibes: {e}")
            nombre_font_name = 'Helvetica-Bold'
        
        # --- Prueba de Plantilla ---
        template_filename = 'plantilla.jpg' 
        template_path = os.path.join(backend_folder, 'static', template_filename)
        if os.path.exists(template_path):
            c.drawImage(template_path, 0, 0, width=width, height=height)
            print(" -> Plantilla OK")
        else:
            print(f" -> ADVERTENCIA: Plantilla no encontrada en {template_path}")

        # --- Prueba de Texto ---
        c.setFont(nombre_font_name, 57)
        c.setFillColor(HexColor('#873233'))
        c.drawCentredString(width / 2.0, 300, "Ana Wonka")
        print(" -> Texto OK")

        c.save()
        print(f"\n¡ÉXITO! Se ha generado el archivo 'TEST_CERTIFICATE.pdf' en la carpeta '{backend_folder}'.")
        print("Por favor, ábrelo y verifica si la plantilla y el texto son correctos.")

    except Exception as e:
        import traceback
        print("\n!!! ERROR CATASTRÓFICO DURANTE LA GENERACIÓN DE PDF AISLADA !!!")
        traceback.print_exc()

if __name__ == '__main__':
    test_generate()