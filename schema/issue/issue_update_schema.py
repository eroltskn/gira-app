from collections import defaultdict
from marshmallow import Schema, fields

from schema.info_schema import InfoSchema
from constant import Constant as CONSTANT


class IssueRequestParameters(object):
    name = 'name'
    description = 'description'
    issue_status_id = 'issue_status_id'
    project_id = 'project_id'
    issue_type_id = 'issue_type_id'


class IssuePatchRequest(object):
    def __init__(self, payload):
        self.name = None
        self.description = None
        self.issue_status_id = None
        self.project_id = None
        self.issue_type_id = None

        if IssueRequestParameters.name in payload:
            self.name = payload[IssueRequestParameters.name]

        if IssueRequestParameters.description in payload:
            self.description = payload[IssueRequestParameters.description]

        if IssueRequestParameters.project_id in payload:
            self.project_id = payload[IssueRequestParameters.project_id]

        if IssueRequestParameters.issue_status_id in payload:
            self.issue_status_id = payload[IssueRequestParameters.issue_status_id]

        if IssueRequestParameters.issue_type_id in payload:
            self.issue_type_id = payload[IssueRequestParameters.issue_type_id]

    def __str__(self):
        return str(self.__dict__)


ISSUE_PATCH_REQUEST_SCHEMA = {
    'name': {'type': 'string'},
    'description': {'type': 'string'},
    'issue_status_id': {'type': 'integer'},
    'issue_type_id': {'type': 'integer'},
}
