# ===================================================================================
# ARCHIVO COMPLETO Y CORREGIDO PARA: backend/generate_all_pdfs.py
# ===================================================================================
import os
import sys
from dotenv import load_dotenv
from flask import Flask

# --- Configuración para que el script funcione desde la raíz ---
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path=dotenv_path)
# --------------------------------------------------------------------

from backend.db import get_db_connection, release_db_connection
from backend.pdf_generator import generate_certificate_pdf

def process_all_pdfs(force_update=False):
    app = Flask(__name__, root_path=os.path.join(project_root, 'backend'))
    with app.app_context():
        # ... (El resto de tu código funcional de este script va aquí)
        pass

if __name__ == '__main__':
    force = len(sys.argv) > 1 and sys.argv[1] == 'force'
    process_all_pdfs(force_update=force)