from flask import Blueprint,request
from utils.response import api_response
from categories.services import fetch_all,create,get_single,update_cat,delete_cat
from categories.schemas import CreateSchema,CategoryResponseSchema
from marshmallow import ValidationError
from flask_jwt_extended import jwt_required,get_jwt_identity,get_jwt


categories_bp=Blueprint("categories",__name__)

@categories_bp.route('/', methods=['GET'])
def get_all():
    """
    Get all categories
    ---
    tags:
      - Categories

    summary: Retrieve all categories

    parameters:
      - name: page
        in: query
        required: false
        type: integer
        default: 1

      - name: per_page
        in: query
        required: false
        type: integer
        default: 10

    responses:
      200:
        description: Categories fetched successfully
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: true
            message:
              type: string
              example: Categories fetched successfully
            data:
              type: array
              items:
                $ref: '#/definitions/Category'
            meta_info:
              type: object
    """
    data = fetch_all()
    data_items=CategoryResponseSchema(many=True).dump(data["items"])

    return api_response(
        data=data_items,
        success=True,
        message="categories fetched successfuly",
        status_code=200,
        meta_info={
            "pagination": data["pagination"]
        }
    )

@categories_bp.route('/',methods=['POST'])
@jwt_required(locations=['headers'])

def create_category():
    """
    Create Category
    ---
    tags:
      - Categories
    security:
      - Bearer: []
    consumes:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - name
          properties:
            name:
              type: string
              example: Electronics

            description:
              type: string
              example: Electronic devices and accessories

    responses:
      201:
        description: Category created successfully
        schema:
          type: object
          properties:
            success:
              type: boolean
            message:
              type: string
            data:
              $ref: '#/definitions/Category'

      401:
        description: Authentication required
    
    """
    try:
        data=CreateSchema().load(request.get_json())
        category=create(data)
        return api_response(
                success=True,
                data=category,
                message='Category created successfuly',
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
 
@categories_bp.route('/<uuid:id>', methods=['GET'])
def get_category(id):
    """
    Get category by id
    ---
    tags:
      - Categories
    summary: Retrieve category by id
    parameters:
      - name: id
        in: path
        required: true
        type: string
        format: uuid
        example: 9e39c0f5-462e-49e2-bb8b-84496f77f274

    responses:
      200:
        description: Category fetched successfully
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: true
            message:
              type: string
              example: Category fetched successfully
            data:
              $ref: '#/definitions/Category'

      404:
        description: Category not found
    """
    try:
        category = get_single(str(id))

        return api_response(
            success=True,
            status_code=200,
            message="Category fetched successfully",
            data=category
        )

    except ValueError as error:
        return api_response(
            success=False,
            message=str(error),
            status_code=404
        )

@categories_bp.route('/<id>',methods=['PUT','PATCH'])
@jwt_required(locations=['headers'])
def update_category(id):
    """
    Update Category
    ---
    tags:
      - Categories
    security:
      - Bearer: []
    consumes:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - name
          properties:
            name:
              type: string
              example: Electronics

            description:
              type: string
              example: Electronic devices and accessories
    responses:
      203:
        description: Category updated successfully
        schema:
          type: object
          properties:
            success:
              type: boolean
            message:
              type: string
            data:
              $ref: '#/definitions/Category'
      401:
        description: Authentication required
    
    
    """
    try:
        data=CreateSchema().load(request.get_json())
        category=update_cat(id=id,data=data)
        return api_response(
            success=True,
            status_code=203,
            message="Category updated successfuly",
            data=category
        )
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
            message=str(error),
            status_code=404
        )
        
@categories_bp.route('/<id>',methods=['DELETE'])
@jwt_required(locations=['headers'])
def delete_category(id):
    """
    Delete category by id
    ---
    tags:
      - Categories
    summary: Delete category by id
    parameters:
      - name: id
        in: path
        required: true
        type: string
        format: uuid
        example: 9e39c0f5-462e-49e2-bb8b-84496f77f274

    responses:
      200:
        description: Category deleted successfully
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: true
            message:
              type: string
              example: Category fetched successfully
      404:
        description: Category not found
    """
    try:
        delete_cat(id)
        
        return api_response(
            success=True,
            status_code=204,
            message="Category deleted successfuly",
        )
    except ValueError as error:
        return api_response(
            success=False,
            message=str(error),
            status_code=500
        )
        
