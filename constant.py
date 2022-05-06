class Constant(object):
    API_HOST = '127.0.0.1'
    API_PORT = 5000

    SQLALCHEMY_DATABASE_URI = "mysql://root:ErolTaskin@localhost:3306/gira"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = 'tobeadded'

    issue_type_defult = 1
    issue_status_defult = 1


