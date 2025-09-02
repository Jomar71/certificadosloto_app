from marshmallow import Schema, fields

class AdminUserSchema(Schema):
    admin_id = fields.Int(dump_only=True)
    login_user = fields.Str(required=True)
    login_pass = fields.Str(required=True, load_only=True)

class CertificateSchema(Schema):
    id_documento = fields.Int(dump_only=True)
    tipo_documento = fields.Str(required=True)
    nombre_persona = fields.Str(required=True)
    apellido_persona = fields.Str(required=True)
    numero_identificacion = fields.Str(required=True)
    fecha_creacion = fields.Date(required=True)
    fecha_vencimiento = fields.Date(required=True)
    ruta_pdf = fields.Str()
    email_persona = fields.Email()

admin_user_schema = AdminUserSchema()
admin_users_schema = AdminUserSchema(many=True)
certificate_schema = CertificateSchema()
certificates_schema = CertificateSchema(many=True)
