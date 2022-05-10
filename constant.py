import os

class Constant(object):
    API_HOST = os.environ.get('API_HOST')
    API_PORT = os.environ.get('API_PORT')
    DEBUG_FLAG = bool(os.environ.get('API_HOST'))

    SQLALCHEMY_DATABASE_URI = os.environ.get('API_HOST')
    SQLALCHEMY_TRACK_MODIFICATIONS = bool(os.environ.get('API_HOST'))

    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')

    ISSUE_TYPE_DEFAULT = 1
    ISSUE_STATUS_DEFAULT = 1

    LOG_FILE_PATH = os.environ.get('LOG_FILE_PATH')

    # default normal user role
    USER_DEFAULT_ROLES = [2]
