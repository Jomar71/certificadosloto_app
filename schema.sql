-- Esquema de la base de datos para la aplicación de certificados

-- Tabla de administradores
CREATE TABLE IF NOT EXISTS administradoresloto (
    id_admin SERIAL PRIMARY KEY,
    login_user VARCHAR(255) UNIQUE NOT NULL,
    login_pass VARCHAR(255) NOT NULL
);

-- Tabla de certificados
CREATE TABLE IF NOT EXISTS certificadosloto (
    id_documento SERIAL PRIMARY KEY,
    tipo_documento VARCHAR(50) NOT NULL,
    nombre_persona VARCHAR(255) NOT NULL,
    apellido_persona VARCHAR(255) NOT NULL,
    numero_identificacion VARCHAR(255) UNIQUE NOT NULL,
    fecha_creacion DATE NOT NULL,
    fecha_vencimiento DATE,
    email_persona VARCHAR(255)
);