from flask import Blueprint, request 
from utils.response import api_response
from listings.services import fetch_all,create_listing,fetch_by_id
from listings.schemas import CreateListingSchema
from marshmallow import ValidationError

listings_bp=Blueprint('listings',__name__)

@listings_bp.route('/',methods=['GET'])
def get_all_listings():
    filters=request.args.to_dict()
    data=fetch_all(filters)

    return api_response(
        data=data["items"],
        success=True,
        message="listings fetched successfuly",
        status_code=200,
        meta_info={
            "pagination":data["pagination"]
        }
    )

@listings_bp.route('/<id>',methods=['GET'])
def get_by_id(id):
    id=id.strip()
    try:
        listing=fetch_by_id(id)
        return api_response(
            data=listing,
            success=True,
            message="listing fetched successfuly",
            status_code=200
        )
    except ValueError as error:
        return api_response(
            success=False,
            message=str(error),
            status_code=404
        )

@listings_bp.route('/',methods=['POST'])
def create():
    try:
        form_data= CreateListingSchema().load(request.get_json())
        listing=create_listing(form_data)
        return api_response(
            success=True,
            data=listing,
            message='Listing created successfuly',
            status_code=201
        )
    except ValidationError as error:
        return api_response(
            success=False,
            message='Error creating listing',
            errors=error.messages,
            status_code=400
        )
    except ValueError as error:
         return api_response(
            success=False,
            message=str(error),
            status_code=400,
        )


    