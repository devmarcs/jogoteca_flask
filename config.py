
SECRET_KEY = 'marc123'

SQLALCHEMY_DATABASE_URI = \
    '{SGBD}://{usuario}:{senha}@{servidor}/{database}'.format(

        SGBD= 'mysql+mysqlconnector',
        usuario= 'marcelo',
        senha= 'admin',
        servidor= 'localhost',
        database= 'jogoteca'
    )