CREATE TABLE administradoresloto (
    id_admin SERIAL PRIMARY KEY,
    login_user VARCHAR(255) UNIQUE NOT NULL,
    login_pass VARCHAR(255) NOT NULL
);

-- Opcional: Insertar un administrador por defecto para poder iniciar sesión
-- Usuario: admin
-- Contraseña: password
INSERT INTO administradoresloto (login_user, login_pass) VALUES ('admin', 'password');