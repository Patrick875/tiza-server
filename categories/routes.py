from flask import Blueprint,request
from utils.response import api_response
from categories.services import fetch_all,create
from categories.schemas import CreateSchema
from marshmallow import ValidationError

categories_bp=Blueprint("categories",__name__)

@categories_bp.route('/',methods=['GET'])
def get_all():
    data=fetch_all()
    return api_response(
        data=data["items"],
        success=True,
        message="categories fetched successfuly",
        status_code=200,
        meta_info={
            "pagination":data["pagination"]
        }
    )

@categories_bp.route('/',methods=['POST'])
def create_category():
    try:
        data=CreateSchema().load(request.get_json())
        category=create(data)
        return api_response(
                success=True,
                data=category,
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