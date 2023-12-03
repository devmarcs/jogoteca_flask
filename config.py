import os

SECRET_KEY = 'marc123'

SQLALCHEMY_DATABASE_URI = \
    '{SGBD}://{usuario}:{senha}@{servidor}/{database}'.format(

        SGBD= 'mysql+mysqlconnector',
        usuario= 'marcelo',
        senha= 'admin',
        servidor= 'localhost',
        database= 'jogoteca'
    )

UPLOAD_PATH = os.path.dirname(os.path.abspath(__file__)) + '/uploads'
UPLOAD_PATH_USER = os.path.dirname(os.path.abspath(__file__)) + '/uploadsUser'
