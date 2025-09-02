
# Admin Users Queries
SELECT_ALL_ADMINS = "SELECT admin_id, login_user FROM admin_users"
SELECT_ADMIN_BY_USERNAME = "SELECT * FROM admin_users WHERE login_user = %s"
INSERT_ADMIN = "INSERT INTO admin_users (login_user, login_pass) VALUES (%s, %s)"
UPDATE_ADMIN = "UPDATE admin_users SET {fields} WHERE admin_id = %s"
DELETE_ADMIN = "DELETE FROM admin_users WHERE admin_id = %s"
SELECT_ANY_ADMIN = "SELECT * FROM admin_users"

# Certificates Queries
SELECT_ALL_CERTIFICATES = "SELECT * FROM certificadosloto"
SELECT_CERTIFICATE_BY_ID = "SELECT * FROM certificadosloto WHERE id_documento = %s"
SELECT_CERTIFICATE_BY_ID_NUMBER = "SELECT * FROM certificadosloto WHERE numero_identificacion = %s"
SELECT_CERTIFICATE_PDF_PATH = "SELECT ruta_pdf FROM certificadosloto WHERE id_documento = %s"
INSERT_CERTIFICATE = "INSERT INTO certificadosloto (tipo_documento, nombre_persona, apellido_persona, numero_identificacion, fecha_creacion, fecha_vencimiento, ruta_pdf, email_persona) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
UPDATE_CERTIFICATE = "UPDATE certificadosloto SET {fields} WHERE id_documento = %s"
DELETE_CERTIFICATE = "DELETE FROM certificadosloto WHERE id_documento = %s"
UPDATE_CERTIFICATE_PDF_PATH = "UPDATE certificadosloto SET ruta_pdf = %s WHERE id_documento = %s"
