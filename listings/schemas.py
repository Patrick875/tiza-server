from marshmallow import Schema,fields,validate
from listings.models import ListingCondition,ListingVerification,LeaseType,ListingStatus,CancelationPolicy
from media.models import MediaType


class IncludedItemSchema(Schema):
    name = fields.String(
        required=True,
        validate=validate.Length(min=1, max=100)
    )

    description = fields.String(
        required=False,
        allow_none=True,
        validate=validate.Length(max=500)
    )

    quantity = fields.Integer(
        required=True,
        validate=validate.Range(min=1)
    )

    price = fields.Float(
        required=False,
        validate=validate.Range(min=0)
    )

class PriceSchema(Schema):
    lease_duration=fields.Integer(required=False,validate=validate.Range(min=0))
    lease_type=fields.String(
        required=True,
            validate=
                validate.OneOf([item.value  for item in LeaseType])
                )
    amount=fields.Float(required=False,validate=validate.Range(min=0))

class MediaInputSchema(Schema):
    name = fields.String(required=False, allow_none=True)

    src = fields.String(required=True)

    alt_text = fields.String(required=False, allow_none=True)

    mime_type = fields.String(required=False, allow_none=True)

    size = fields.Integer(
        required=False,
        allow_none=True,
        validate=validate.Range(min=0)
    )

    duration = fields.Integer(
        required=False,
        allow_none=True,
        validate=validate.Range(min=0)
    )

    thumbnail = fields.String(required=False, allow_none=True)

    type = fields.String(
        required=False,
        load_default=MediaType.IMAGE.value,
        validate=validate.OneOf([item.value for item in MediaType])
    )

class CreateListingSchema(Schema):
    name=fields.String(required=True,validate=[validate.Length(min=3,max=100)])
    category_id=fields.Integer(required=True)
    display_image=fields.Nested(MediaInputSchema,required=True)
    media=fields.List(fields.Nested(MediaInputSchema),load_default=list)
    description=fields.String(
        required=False,
        allow_none=True,
        validate=[validate.Length(min=3)]
        )
    listing_verification=fields.String(required=False,
        load_default=ListingVerification.PENDING.value,
        validate=validate.OneOf([item.value for item in ListingVerification])
        )
    condition=fields.String(
        required=True,
        validate=[validate.OneOf([item.value for item in ListingCondition])]
    )

    tags=fields.List(
        fields.String(
       required=False,
       load_default=list,
       validate=validate.Length(min=1,max=50)
       ))
    
    included_items=fields.List(
        fields.Nested(IncludedItemSchema),
        load_default=list,
        required=False
    )
    leasing_types=fields.List(
        fields.String(
            validate=
                validate.OneOf([item.value  for item in LeaseType])
                ),
                required=False,
                load_default=list
                )
    
    primary_lease_type= fields.String(
            required=True,
            validate=
                validate.OneOf([item.value  for item in LeaseType])
                )
    security_deposit=fields.Float(required=False, validate=validate.Range(min=0),load_default=0)
    status=fields.String(required=True, validate=[validate.OneOf([item.value for item in ListingStatus])])
    available_from=fields.DateTime(required=False)
    available_to=fields.DateTime(required=False)
    minimum_rental_period=fields.Integer(required=False,validate=validate.Range(min=0))
    maximum_rental_period=fields.Integer(required=False,validate=validate.Range(min=0))
    delivery_available= fields.Boolean(required=False,load_default=False)
    delivery_fee=fields.Float(required=False, validate=validate.Range(min=0),load_default=0)
    cancellation_policy=fields.String(required=True, validate=[validate.OneOf([item.value for item in CancelationPolicy])])
    contract=fields.Nested(MediaInputSchema,required=False)
    prices=fields.List(fields.Nested(PriceSchema),required=True)
    lessor_id =fields.Integer(required=True)
