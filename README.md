# App de Certificados

Este proyecto es una aplicación web completa para la gestión y distribución de certificados. Permite a los usuarios públicos buscar y descargar sus certificados, y ofrece un panel de administración robusto para la gestión completa de los registros.

La aplicación está desplegada y funcional:
*   **Frontend Público:** [https://jomar71.github.io/certificadosloto_app/](https://jomar71.github.io/certificadosloto_app/)
*   **API del Backend:** [https://certificadosloto-app.onrender.com](https://certificadosloto-app.onrender.com)

## Características Principales

### Módulo de Usuario (Público)
*   **Búsqueda de Certificados:** Los usuarios pueden buscar certificados ingresando su número de cédula.
*   **Visualización y Descarga en PDF:** Permite visualizar y descargar el certificado oficial en formato PDF, generado con una plantilla personalizada.

### Módulo de Administración
*   **Autenticación Segura:** Acceso restringido para administradores mediante usuario y contraseña.
*   **Gestión de Certificados:**
    *   Listar todos los certificados existentes en la base de datos.
    *   Crear nuevos registros de certificados.
    *   Editar la información de certificados existentes.
    *   Generar y regenerar los archivos PDF asociados a cada certificado.

## Tecnologías Utilizadas

*   **Backend:** Python 3.11, Flask, Gunicorn
*   **Frontend:** HTML5, CSS3, JavaScript (Vanilla JS)
*   **Base de Datos:** PostgreSQL
*   **Librerías Clave:**
    *   `psycopg2-binary`: Conector para PostgreSQL.
    *   `Flask-Cors`: Para gestionar la comunicación entre frontend y backend.
    *   `ReportLab`: Para la generación de los documentos PDF.
    *   `Alembic`: Para gestionar las migraciones de la base de datos.
    *   `python-dotenv`: Para manejar variables de entorno.
*   **Despliegue:**
    *   Frontend desplegado en **GitHub Pages**.
    *   Backend y Base de Datos desplegados en **Render.com**.

## Estructura Final del Proyecto

La estructura fue refactorizada para un despliegue estándar y robusto.
certificadolotogemini/
├── app.py # Archivo principal de Flask (en la raíz)
├── requirements.txt # Dependencias de Python (en la raíz)
├── runtime.txt # Especifica la versión de Python para Render (en la raíz)
├── .gitignore
├── README.md
│
├── backend/
│ ├── .env # Archivo de configuración local (NO SUBIR A GITHUB)
│ ├── alembic.ini # Configuración de Alembic
│ ├── auth.py
│ ├── create_admin.py # Script para crear el usuario admin
│ ├── db.py
│ ├── pdf_generator.py # Lógica para crear los PDFs
│ │
│ ├── certificates_generated/ # PDFs generados (ignorado por Git)
│ ├── fonts/ # Fuentes personalizadas para los PDFs
│ ├── migrations/ # Archivos de migración de Alembic
│ ├── static/ # Plantilla de imagen para los PDFs
│ └── routes/ # Archivos de rutas (admin, certificate, main)
│
└── frontend/
├── index.html
├── style.css
├── script.js
└── config.js```
Guía de Instalación y Ejecución Local
Sigue estos pasos para correr el proyecto en tu propia computadora.
Requisitos Previos
Git instalado.
Python 3.11 instalado (y añadido al PATH).
Node.js instalado (para la herramienta de despliegue gh-pages).
PostgreSQL instalado y el servicio corriendo.

1. Configuración del Backend
Clona el repositorio y navega a la carpeta raíz del proyecto.
Crea el entorno virtual usando Python 3.11:
Bash
py -3.11 -m venv backend/venv

Activa el entorno virtual:
Bash
source backend/venv/Scripts/activate

Instala las dependencias de Python:
Bash
pip install -r requirements.txt

Configura las variables de entorno:
Crea un archivo llamado .env dentro de la carpeta backend/.
Pega el siguiente contenido y rellena tus datos:
Env
SECRET_KEY="una-clave-secreta-muy-larga-y-segura"
DATABASE_URL="postgresql://tu_usuario:tu_contraseña@localhost:5432/bd_certilotos"

Crea las tablas en la base de datos:
Navega a la carpeta del backend: cd backend

Ejecuta Alembic: alembic upgrade head
Vuelve a la raíz: cd ..

Crea tu usuario administrador:
Bash
python backend/create_admin.py

2. Configuración del Frontend
Abre el archivo frontend/config.js.
Asegúrate de que la URL apunte a tu servidor local:

JavaScript
const API_BASE_URL = 'http://127.0.0.1:5000';

3. ¡Poner a Funcionar la App!
Siempre necesitarás dos servidores corriendo al mismo tiempo.

Para iniciar el Backend (el cerebro):
Abre una terminal en la raíz del proyecto.

Activa el entorno: source backend/venv/Scripts/activate
Ejecuta: python app.py

Deja esta terminal abierta.

Para iniciar el Frontend (la cara):

En VS Code, haz clic derecho sobre frontend/index.html.
Selecciona "Open with Live Server".
¡Ahora tu aplicación estará funcionando localmente!
Personalización del Certificado

Para cambiar la apariencia (posición, fuentes, colores, textos) de los certificados generados, edita la "ZONA DE PERSONALIZACIÓN" que se encuentra dentro del archivo backend/pdf_generator.py. Después de cada cambio, deberás reiniciar manualmente el servidor del backend para ver los resultados.



