from collections import defaultdict
from marshmallow import Schema, fields

from schema.info_schema import InfoSchema


class ProjectAssignRequestParameters(object):
    user_id = 'user_id'
    project_id = 'project_id'


class ProjectAssignPostRequest(object):
    def __init__(self, payload):
        self.name = None
        self.created_by = None

        if ProjectAssignRequestParameters.user_id in payload:
            self.user_id = payload[ProjectAssignRequestParameters.user_id]

        if ProjectAssignRequestParameters.project_id in payload:
            self.project_id = payload[ProjectAssignRequestParameters.project_id]


    def __str__(self):
        return str(self.__dict__)


PROJECT_ASSIGN_POST_REQUEST_SCHEMA = {
    'project_id': {'type': 'integer', 'required': True},
    'user_id': {'type': 'integer', 'required': True},
}
