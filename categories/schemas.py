from marshmallow import Schema,validate,fields

class CreateSchema(Schema):
    name=fields.String(validate=validate.Length(min=2,max=100))
    description=fields.String()

class CategoryResponseSchema(Schema):
    id = fields.Str()
    name = fields.Str()
    description = fields.Str()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()