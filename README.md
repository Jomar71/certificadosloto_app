# App de Certificados

Este proyecto es una aplicación web completa para la gestión y distribución de certificados. Permite a los usuarios buscar y descargar sus certificados, y ofrece un panel de administración robusto para la gestión de usuarios administradores y certificados.

## Características Principales

### Módulo de Usuario (Público)
*   **Búsqueda de Certificados:** Los usuarios pueden buscar certificados ingresando su número de cédula.
*   **Visualización de Detalles:** Muestra información relevante del certificado encontrado.
*   **Descarga en PDF:** Permite descargar el certificado en formato PDF.
*   **Envío por Correo Electrónico:** Opción para enviar el certificado a una dirección de email.

### Módulo de Administración
*   **Autenticación Segura:** Acceso restringido para administradores.
*   **Gestión de Administradores:**
    *   Creación, edición y eliminación de cuentas de administrador.
*   **Gestión de Certificados:**
    *   Creación, edición y eliminación de registros de certificados.
    *   Generación automática de archivos PDF para los certificados.

## Tecnologías Utilizadas

### Backend (Python - Flask)
*   **Flask:** Microframework web para Python.
*   **Flask-Cors:** Extensión para manejar Cross-Origin Resource Sharing (CORS).
*   **python-dotenv:** Para la gestión de variables de entorno.
*   **ReportLab:** Librería para la generación de documentos PDF.
*   **psycopg2-binary:** Adaptador de PostgreSQL para Python.
*   **Alembic:** Herramienta de migraciones de base de datos para SQLAlchemy (utilizado con PostgreSQL).

### Frontend (HTML, CSS, JavaScript)
*   **HTML5:** Estructura de la aplicación web.
*   **CSS3:** Estilos y diseño responsivo.
*   **JavaScript (Vanilla JS):** Lógica interactiva del lado del cliente.
*   **config.js:** Archivo de configuración para la URL base de la API.

## Estructura del Proyecto

El proyecto está dividido en dos directorios principales:

*   `backend/`: Contiene toda la lógica del servidor, la API RESTful, la gestión de la base de datos, la autenticación y la generación de certificados.
    *   `app.py`: Punto de entrada de la aplicación Flask.
    *   `auth.py`: Lógica de autenticación.
    *   `db.py`: Configuración de la base de datos.
    *   `schemas.py`: Definiciones de esquemas de datos.
    *   `routes/`: Módulos para las diferentes rutas de la API (main, admin, certificate).
    *   `migrations/`: Archivos de migración de la base de datos (Alembic).
    *   `certificates_generated/`: Directorio donde se guardan los PDFs de los certificados generados.
    *   `fonts/`: Fuentes utilizadas para la generación de PDFs.
*   `frontend/`: Contiene la interfaz de usuario de la aplicación web.
    *   `index.html`: Página principal de la aplicación.
    *   `style.css`: Hoja de estilos.
    *   `script.js`: Lógica del lado del cliente para interactuar con el backend.
    *   `config.js`: Configuración del frontend, como la URL de la API.

## Instalación y Configuración

Para poner en marcha el proyecto, sigue los siguientes pasos:

### 1. Clonar el Repositorio
```bash
git clone <URL_DEL_REPOSITORIO>
cd certificadolotogemini
```

### 2. Configuración del Backend

Navega al directorio `backend`:
```bash
cd backend
```

**Crear un entorno virtual e instalar dependencias:**
```bash
python -m venv venv
source venv/bin/activate  # En Linux/macOS
# o
venv\Scripts\activate     # En Windows
pip install -r requirements.txt
```

**Configurar variables de entorno:**
Crea un archivo `.env` en el directorio `backend/` con las siguientes variables (ejemplo):
```
SECRET_KEY="tu_clave_secreta_aqui"
DATABASE_URL="postgresql://user:password@host:port/database_name"
ADMIN_USERNAME="admin"
ADMIN_PASSWORD="password"
EMAIL_HOST="smtp.example.com"
EMAIL_PORT="587"
EMAIL_USERNAME="your_email@example.com"
EMAIL_PASSWORD="your_email_password"
```
Asegúrate de reemplazar los valores con tu configuración real de base de datos y correo electrónico.

**Inicializar y aplicar migraciones de la base de datos:**
```bash
alembic upgrade head
```

**Ejecutar el backend:**
```bash
flask run
# o
python app.py
```
El servidor backend se ejecutará en `http://127.0.0.1:5000` por defecto.

### 3. Configuración del Frontend

Navega al directorio `frontend`:
```bash
cd frontend
```

**Configurar la URL de la API:**
Abre `config.js` y asegúrate de que `API_BASE_URL` apunte a la dirección de tu backend (por defecto, `http://127.0.0.1:5000`).
```javascript
// frontend/config.js
const API_BASE_URL = 'http://127.0.0.1:5000';
```

**Abrir la aplicación:**
Simplemente abre el archivo `index.html` en tu navegador web.

## Uso

### Para Usuarios
1.  Abre `frontend/index.html` en tu navegador.
2.  Ingresa un número de cédula en el campo de búsqueda.
3.  Si se encuentra el certificado, podrás verlo, descargarlo o enviarlo por correo.

### Para Administradores
1.  Haz clic en "Iniciar Sesión" en la barra de navegación.
2.  Ingresa las credenciales de administrador configuradas en el archivo `.env`.
3.  Una vez autenticado, haz clic en "Panel de Administración" para acceder a las funciones de gestión.