from collections import defaultdict
from marshmallow import Schema, fields

from schema.info_schema import InfoSchema


class UserRegisterRequestParameters(object):
    username = 'username'
    password = 'password'
    email = 'email'
    first_name = 'first_name'
    last_name = 'last_name'


class UserRegisterPostRequest(object):
    def __init__(self, payload):
        self.username = None
        self.password = None

        if UserRegisterRequestParameters.username in payload:
            self.username = payload[UserRegisterRequestParameters.username]

        if UserRegisterRequestParameters.password in payload:
            self.password = payload[UserRegisterRequestParameters.password]

        if UserRegisterRequestParameters.email in payload:
            self.email = payload[UserRegisterRequestParameters.email]

        if UserRegisterRequestParameters.first_name in payload:
            self.first_name = payload[UserRegisterRequestParameters.first_name]

        if UserRegisterRequestParameters.last_name in payload:
            self.last_name = payload[UserRegisterRequestParameters.last_name]

    def __str__(self):
        return str(self.__dict__)


class UserRegisterResponse(object):
    def __init__(self, gira_token=None):
        self.info = defaultdict(dict)
        self.data = defaultdict(dict)

        self.info['data'] = True
        self.info['errors'] = False

        self.data['gira_token'] = gira_token

    def __iter__(self):
        return UserRegisterResponseSchema(many=False).dump(self).data

    def __str__(self):
        return str(self.__dict__)


class UserRegisterResultSchema(Schema):
    gira_token = fields.String()


class UserRegisterResponseSchema(Schema):
    info = fields.Nested(InfoSchema)
    data = fields.Nested(UserRegisterResultSchema)


USER_REGISTER_POST_REQUEST_SCHEMA = {
    'username': {'type': 'string', 'required': True},
    'password': {'type': 'string', 'required': True},
    'email': {'type': 'string', 'required': True},
    'first_name': {'type': 'string', 'required': True},
    'last_name': {'type': 'string', 'required': True},
}
