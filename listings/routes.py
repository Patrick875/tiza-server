from flask import Blueprint, request 
from utils.response import api_response
from listings.services import fetch_all_public,fetch_all_per_category,create_listing,fetch_by_id,update_listing,delete_listing,fetch_all_for_user
from listings.schemas import CreateListingSchema,UpdateListingSchema
from marshmallow import ValidationError
from flask_jwt_extended import jwt_required,get_jwt_identity,get_jwt

listings_bp=Blueprint('listings',__name__)



@listings_bp.route('/',methods=['GET'])
def get_all_listings():
    filters=request.args.to_dict()
    data=fetch_all_public(filters)

    return api_response(
        data=data["items"],
        success=True,
        message="listings fetched successfuly",
        status_code=200,
        meta_info={
            "pagination":data["pagination"]
        }
    )
@listings_bp.route('/category/<id>',methods=['GET'])
def get_all_listings_per_category(id:str):
    categ_id=id.strip()
    filters=request.args.to_dict()
    data=fetch_all_per_category(filters=filters,category_id=categ_id)

    return api_response(
        data=data["items"],
        success=True,
        message="listings fetched successfuly",
        status_code=200,
        meta_info={
            "pagination":data["pagination"]
        }
    )
@listings_bp.get("/mine")
@jwt_required(locations=['headers'])
def get_user_listings():
    filters = request.args.to_dict()

    user_id = int(get_jwt_identity())
    claims = get_jwt()
    roles = claims.get("roles", [])

    data = fetch_all_for_user(filters, user_id, roles)

    return api_response(
        success=True,
        message="Listings fetched successfully",
        data=data["items"],
        meta_info={"pagination": data["pagination"]},
        status_code=200
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
@jwt_required(locations=['headers'])
def create():
    try:
        form_data= CreateListingSchema().load(request.get_json())
        user_id=int(get_jwt_identity())
        form_data["lessor_id"]=user_id
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

@listings_bp.route('/<id>',methods=['PUT','PATCH'])
@jwt_required(locations=['headers'])
def update(id:str):
    try:
        data=UpdateListingSchema().load(request.get_json())
        listing= update_listing(id,data)
        return api_response(success=True,
            data=listing,
            message='Listing updated successfuly',
            status_code=203)
    except ValidationError as error:
        return api_response(
            success=False,
            message='Error updating listing',
            errors=error.messages,
            status_code=400
        )
    except ValueError as error:
        return api_response(
            success=False,
            status_code=400,
            message=str(error)
        )
    
@listings_bp.route('/<id>',methods=['DELETE'])
@jwt_required(locations=['headers'])
def delete_list(id):
    try:
        user_id=int(get_jwt_identity())
        roles=get_jwt().get("roles",[])
        is_admin= 'ADMIN' in roles

        listing=delete_listing(id,user_id,is_admin)
        
        return api_response(
            success=True,
            message="Listing deleted successfully",
            status_code=200
        )

    except ValueError as error:
        return api_response(
            success=False,
            message=str(error),
            status_code=404
        )




    