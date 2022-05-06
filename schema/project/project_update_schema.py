from collections import defaultdict
from marshmallow import Schema, fields

from schema.info_schema import InfoSchema
from constant import Constant as CONSTANT


class ProjectRequestParameters(object):
    name = 'name'


class ProjectPatchRequest(object):
    def __init__(self, payload):
        self.name = None

        if ProjectRequestParameters.name in payload:
            self.name = payload[ProjectRequestParameters.name]


    def __str__(self):
        return str(self.__dict__)


PROJECT_PATCH_REQUEST_SCHEMA = {
    'name': {'type': 'string'},
}
