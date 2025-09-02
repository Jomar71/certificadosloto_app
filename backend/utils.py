import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from dotenv import load_dotenv

load_dotenv()

# --- Registrar Fuentes ---
try:
    # Fuente para nombres y apellidos
    great_vibes_path = os.path.join(os.path.dirname(__file__), 'fonts', 'GreatVibes-Regular.ttf')
    pdfmetrics.registerFont(TTFont('Great Vibes', great_vibes_path))

    # Fuente para cédula y fechas
    garet_path = os.path.join(os.path.dirname(__file__), 'fonts', 'Garet-Book.otf')
    pdfmetrics.registerFont(TTFont('Garet', garet_path))
except Exception as e:
    print(f"ADVERTENCIA: No se pudieron cargar las fuentes personalizadas. Se usarán fuentes estándar. Error: {e}")

def generate_certificate_pdf(certificate_data, output_path):
    """
    Genera un certificado en formato PDF con los datos proporcionados,
    usando una plantilla de fondo y fuentes personalizadas.
    """
    c = canvas.Canvas(output_path, pagesize=letter)
    width, height = letter

    # --- Dibujar Plantilla de Fondo ---
    template_image_path = os.path.join(os.path.dirname(__file__), 'templates', 'certificates', 'certificados_loto_app.png')
    if os.path.exists(template_image_path):
        img = ImageReader(template_image_path)
        c.drawImage(img, 0, 0, width=width, height=height, preserveAspectRatio=True, anchor='c')
    else:
        print(f"ADVERTENCIA: La imagen de plantilla no se encontró en {template_image_path}. Se generará un certificado sin fondo.")

    # --- Colores ---
    gold_color = HexColor("#a89a5b")

    # --- Escribir Nombre y Apellido ---
    # Combina nombre y apellido y los pone en formato de título (Mayúscula Cada Palabra)
    full_name = f"{certificate_data['nombre_persona']} {certificate_data['apellido_persona']}".title()
    try:
        c.setFont('Great Vibes', 48)
        c.setFillColor(gold_color)
        # Ajusta la posición Y (450) según sea necesario para tu plantilla
        c.drawCentredString(width / 2.0, 450, full_name)
    except Exception as e:
        print(f"Error al usar la fuente 'Great Vibes'. Usando Helvetica. Error: {e}")
        c.setFont('Helvetica-Bold', 30) # Fallback
        c.drawCentredString(width / 2.0, 450, full_name)


    # --- Escribir Número de Cédula ---
    id_number_text = f"C.C. {certificate_data['numero_identificacion']}"
    try:
        c.setFont('Garet Book', 14)
        c.setFillColor(gold_color)
        # Ajusta la posición Y (390) según sea necesario
        c.drawCentredString(width / 2.0, 390, id_number_text)
    except Exception as e:
        print(f"Error al usar la fuente 'Garet Book'. Usando Helvetica. Error: {e}")
        c.setFont('Helvetica', 12) # Fallback
        c.drawCentredString(width / 2.0, 390, id_number_text)


    # --- Escribir Fechas ---
    try:
        c.setFont('Garet Book', 12)
        c.setFillColor(gold_color)
        # Ajusta las posiciones X e Y según sea necesario
        c.drawString(inch, 2.5 * inch, f"Fecha de Emisión: {certificate_data['fecha_creacion']}")
        c.drawRightString(width - inch, 2.5 * inch, f"Fecha de Vencimiento: {certificate_data['fecha_vencimiento']}")
    except Exception as e:
        print(f"Error al usar la fuente 'Garet Book'. Usando Helvetica. Error: {e}")
        c.setFont('Helvetica', 10) # Fallback
        c.drawString(inch, 2.5 * inch, f"Fecha de Emisión: {certificate_data['fecha_creacion']}")
        c.drawRightString(width - inch, 2.5 * inch, f"Fecha de Vencimiento: {certificate_data['fecha_vencimiento']}")


    c.save()
    return output_path

def send_email_with_attachment(recipient_email, subject, body, attachment_path=None):
    """
    Envía un correo electrónico con un archivo adjunto.
    """
    sender_email = os.environ.get('EMAIL_USER')
    sender_password = os.environ.get('EMAIL_PASS')
    smtp_server = os.environ.get('SMTP_SERVER')
    smtp_port = int(os.environ.get('SMTP_PORT', 587))

    if not all([sender_email, sender_password, smtp_server]):
        raise ValueError("Configuración de correo electrónico incompleta en .env")

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    if attachment_path and os.path.exists(attachment_path):
        with open(attachment_path, "rb") as f:
            attach = MIMEApplication(f.read(), _subtype="pdf")
            attach.add_header('Content-Disposition', 'attachment', filename=os.path.basename(attachment_path))
            msg.attach(attach)

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
        return True
    except Exception as e:
        print(f"Error al enviar correo: {e}")
        raise
    return False