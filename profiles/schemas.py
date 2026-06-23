from marshmallow import Schema,fields

class CreateLessorProfileSchema(Schema):
    display_name = fields.String(required=True),
    business_type = fields.String(required=True),
    verification_status = fields.String(required=False),
    preferred_listing_categories = fields.List(fields.String(),required=False),
    payout_phone = fields.String(required=True),
    payout_bank_name = fields.String(required=False),
    payout_account_number = fields.String(required=False)

class UpdateProfileSchema(Schema):
    display_name = fields.String(required=False),
    business_type = fields.String(required=False),
    verification_status = fields.String(required=False),
    preferred_listing_categories = fields.String(required=False),
    payout_phone = fields.String(required=False),
    payout_bank_name = fields.String(required=False),
    payout_account_number = fields.String(required=False),
    total_listings = fields.String(required=False) 

class UpdateProfileSchemaStatus(Schema):
    status = fields.String(required=True)  