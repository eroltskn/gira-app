from collections import defaultdict
from marshmallow import Schema, fields

from schema.info_schema import InfoSchema
from constant import Constant as CONSTANT


class ProjectRequestParameters(object):
    name = 'name'
    created_by = 'created_by'


class ProjectPostRequest(object):
    def __init__(self, payload):
        self.name = None
        self.created_by = None

        if ProjectRequestParameters.name in payload:
            self.name = payload[ProjectRequestParameters.name]

        if ProjectRequestParameters.created_by in payload:
            self.created_by = payload[ProjectRequestParameters.created_by]


    def __str__(self):
        return str(self.__dict__)


PROJECT_POST_REQUEST_SCHEMA = {
    'name': {'type': 'string', 'required': True},
    'created_by': {'type': 'integer', 'required': True},
}
