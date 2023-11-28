
SECRET_KEY = 'marc123'

SQLALCHEMY_DATABASE_URI = \
    '{SGBD}://{usuario}:{senha}@{servidor}/{database}'.format(

        SGBD= 'mysql+mysqlconnector',
        usuario= 'root',
        senha= '',
        servidor= 'localhost',
        database= 'jogoteca'
    )