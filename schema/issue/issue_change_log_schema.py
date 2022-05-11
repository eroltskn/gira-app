
class IssueRequestParameters(object):
    id = 'id'
    field_name = 'field_name'
    new_value = 'new_value'
    issue_id = 'issue_id'
    user_id = 'user_id'


class IssueChangeLogPostRequest(object):
    def __init__(self, payload):
        self.id = None
        self.field_name = None
        self.new_value = None
        self.issue_id = None
        self.user_id = None

        if IssueRequestParameters.id in payload:
            self.id = payload[IssueRequestParameters.id]

        if IssueRequestParameters.field_name in payload:
            self.field_name = payload[IssueRequestParameters.field_name]

        if IssueRequestParameters.new_value in payload:
            self.new_value = payload[IssueRequestParameters.new_value]

        if IssueRequestParameters.issue_id in payload:
            self.issue_id = payload[IssueRequestParameters.issue_id]

        if IssueRequestParameters.user_id in payload:
            self.user_id = payload[IssueRequestParameters.user_id]

    def __str__(self):
        return str(self.__dict__)


ISSUE_CHANGE_LOG_POST_REQUEST_SCHEMA = {
    'issue_id': {'type': 'integer', 'required': True},
    'user_id': {'type': 'integer', 'required': True},
    'field_name': {'type': 'string', 'required': True},
    'new_value': {'type': 'string'},
}
