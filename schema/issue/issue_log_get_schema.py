from collections import defaultdict
from marshmallow import Schema, fields

from schema.info_schema import InfoSchema


class IssueLogGetResponse(object):
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
        return IssueLogGetResponseSchema(many=False).dump(self).data

    def __str__(self):
        return str(self.__dict__)


class IssueLogResultSchema(Schema):
    id = fields.String()
    field_name = fields.String()
    new_value = fields.String()
    old_value = fields.Integer()
    user_id = fields.Integer()
    issue_id = fields.Integer()
    created = fields.String()
    updated = fields.String()


class IssueLogGetResponseSchema(Schema):
    info = fields.Nested(InfoSchema)
    data = fields.List(fields.Nested(IssueLogResultSchema))

