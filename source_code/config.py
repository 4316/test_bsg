import os

PROJECT = 'test'
PROJECT_ROOT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
CSRF_ENABLED = True
SECRET_KEY = "ys)g*1u-*g@^k@mh&)!68*w!m(88$48w34r*6gedeqhd#_tdws"
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + PROJECT_ROOT + '/db.sqlite'
REMEMBER_COOKIE_DURATION = 600

sql_param = {
    'convert_unicode': True,
    'echo': False,
}
db_session_param = {
    'autocommit': False,
    'autoflush': False,
}
