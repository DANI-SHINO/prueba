import os
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'clave-secreta-super-segura'

    SQLALCHEMY_DATABASE_URI = (
        'mysql+pymysql://avnadmin:AVNS_xlj5WYOprcR-tFN6xX1@'
        'mysql-1b6c1203-mirandadiazjesusdaniel-8cf4.k.aivencloud.com:21093/defaultdb'
    )

    SQLALCHEMY_ENGINE_OPTIONS = {
        'connect_args': {
            'ssl': {
                'ssl_verify_cert': False,     # 👈 evita verificación de cert
                'ssl_check_hostname': False   # 👈 evita verificación de hostname
            }
        }
    }

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = 'sandbox.smtp.mailtrap.io'
    MAIL_PORT = 2525
    MAIL_USE_TLS = True
    MAIL_USERNAME = '5941fdd25fae2b'
    MAIL_PASSWORD = 'd4e6b9abc0517e'

