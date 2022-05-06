from collections import defaultdict
from marshmallow import Schema, fields

from schema.info_schema import InfoSchema


class IssueGetResponse(object):
    def __init__(self, result=None):
        self.info = defaultdict(dict)
        self.data = defaultdict(dict)

        self.info['data'] = True
        self.info['errors'] = False

        if result is None or len(result) == 0:
            self.info['data'] = False
        else:
            self.info['data'] = True
            self.data = result

    def __iter__(self):
        return IssueGetResponseSchema(many=False).dump(self).data

    def __str__(self):
        return str(self.__dict__)


class IssueResultSchema(Schema):
    id = fields.String()
    name = fields.String()
    description = fields.String()
    project_id = fields.Integer()
    issue_status_id = fields.Integer()
    issue_type_id = fields.Integer()
    created = fields.String()
    updated = fields.String()


class IssueGetResponseSchema(Schema):
    info = fields.Nested(InfoSchema)
    data = fields.Nested(IssueResultSchema)

