from marshmallow import Schema,validate,fields

class CreateSchema(Schema):
    name=fields.String(validate=validate.Length(min=2,max=100))
    description=fields.String()