class Constant(object):
    API_HOST = '127.0.0.1'
    API_PORT = 5000
    DEBUG_FLAG = True

    SQLALCHEMY_DATABASE_URI = "mysql://root:ErolTaskin@localhost:3306/gira"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # TODO Will be replaced with env variable
    JWT_SECRET_KEY = 'tobeadded'

    ISSUE_TYPE_DEFAULT = 1
    ISSUE_STATUS_DEFAULT = 1

    LOG_FILE_PATH = 'C:\\Users\\erol_\\Documents\\Browzzin\\gira-app'

    # default normal user role
    USER_DEFAULT_ROLES = [2]
