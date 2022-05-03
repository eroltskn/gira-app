from collections import defaultdict
from marshmallow import Schema, fields

from schema.info_schema import InfoSchema


class UserAuthRequestParameters(object):
    username = 'username'
    password = 'password'


class UserAuthPostRequest(object):
    def __init__(self, payload):
        self.username = None
        self.password = None

        if UserAuthRequestParameters.username in payload:
            self.username = payload[UserAuthRequestParameters.username]

        if UserAuthRequestParameters.password in payload:
            self.password = payload[UserAuthRequestParameters.password]

    def __str__(self):
        return str(self.__dict__)


class UserAuthResponse(object):
    def __init__(self, gira_token=None):
        self.info = defaultdict(dict)
        self.data = defaultdict(dict)

        self.info['data'] = True
        self.info['errors'] = False

        self.data['gira_token'] = gira_token

    def __iter__(self):
        return UserAuthResponseSchema(many=False).dump(self).data

    def __str__(self):
        return str(self.__dict__)


class UserAuthResultSchema(Schema):
    gira_token = fields.String()


class UserAuthResponseSchema(Schema):
    info = fields.Nested(InfoSchema)
    data = fields.Nested(UserAuthResultSchema)


USER_AUTH_POST_REQUEST_SCHEMA = {
    'username': {'type': 'string', 'required': True},
    'password': {'type': 'string', 'required': True},
}
