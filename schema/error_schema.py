from collections import defaultdict

from marshmallow import Schema, fields

from schema.info_schema import InfoSchema


class ErrorSchema(Schema):
    info = fields.Nested(InfoSchema)
    errors = fields.List(fields.String())


class ErrorResponse(object):
    def __init__(self,  errors):
        self.info = defaultdict(dict)

        self.info['errors'] = True
        self.info['data'] = False

        if type(errors) is not list:
            errors = [errors]

        self.errors = errors

    def __iter__(self):
        return ErrorSchema(many=False).dump(self).data

    def __str__(self):
        return str(self.__dict__)
