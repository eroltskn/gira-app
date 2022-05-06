from collections import defaultdict
from marshmallow import Schema, fields

from schema.info_schema import InfoSchema
from constant import Constant as CONSTANT


class ProjectRequestParameters(object):
    name = 'name'
    assign_to = 'assign_to'


class ProjectPatchRequest(object):
    def __init__(self, payload):
        self.name = None
        self.assign_by = None
        self.assign_to = None

        if ProjectRequestParameters.name in payload:
            self.name = payload[ProjectRequestParameters.name]

        if ProjectRequestParameters.assign_to in payload:
            self.assign_to = payload[ProjectRequestParameters.assign_to]


    def __str__(self):
        return str(self.__dict__)


PROJECT_PATCH_REQUEST_SCHEMA = {
    'name': {'type': 'string'},
    'assign_to': {'type': 'integer'},
}
