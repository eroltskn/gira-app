from collections import defaultdict
from marshmallow import Schema, fields

from schema.info_schema import InfoSchema


class ProjectGetResponse(object):
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
        return ProjectGetResponseSchema(many=False).dump(self).data

    def __str__(self):
        return str(self.__dict__)


class ProjectResultSchema(Schema):
    id = fields.String()
    name = fields.String()
    created = fields.String()
    updated = fields.String()
    created_by = fields.String()
    issue_count = fields.Integer()


class ProjectGetResponseSchema(Schema):
    info = fields.Nested(InfoSchema)
    data = fields.Nested(ProjectResultSchema)

