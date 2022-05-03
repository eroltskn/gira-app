from collections import defaultdict

from marshmallow import Schema, fields


class InfoSchema(Schema):
    code = fields.Integer()
    errors = fields.Boolean()
    data = fields.Boolean()


class InfoResponseSchema(Schema):
    info = fields.Nested(InfoSchema)


class InfoResponse(object):
    def __init__(self,  errors=False, data=False):
        self.info = defaultdict(dict)

        self.info['errors'] = errors
        self.info['data'] = data

    def __iter__(self):
        return InfoResponseSchema(many=False).dump(self).data

    def __str__(self):
        return str(self.__dict__)
