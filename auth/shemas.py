from marshmallow import fields,Schema,validate
from utils.validators import validate_password

class SignupSchema(Schema):
    email=fields.Email(required=True)
    password=fields.String(required=True,load_only=True,validate=validate_password)
    first_name = fields.String(required=True,validate=[validate.Length(min=3,max=30),validate.Regexp(
                r"^[A-Za-z]+$",
                error="First name must contain only alphabetical characters"
            )])
    last_name = fields.String(required=True,validate=[validate.Length(min=3,max=30),validate.Regexp(
                r"^[A-Za-z]+$",
                error="Last name must contain only alphabetical characters"
            )])
    phone = fields.String(required=False, allow_none=True)

class LoginSchema(Schema):
    email=fields.Email(required=True)
    password=fields.String(required=True)