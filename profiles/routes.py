from flask import Blueprint,request
from flask_jwt_extended import jwt_required,get_jwt_identity
from profiles.services import get_user_profiles,update_lessor_profile,add_lessor_profile,update_lessor_profile_status
from utils.response import api_response
from profiles.schemas import UpdateProfileSchema,CreateLessorProfileSchema,UpdateProfileSchemaStatus


profiles_bp=Blueprint('profiles',__name__)

@profiles_bp.route("/me",methods=['GET'])
@jwt_required(locations=['headers','cookies'])
def get_my_profiles():
    """
    Get current user profiles
    ---
    description: Return user profiles
    tags:
      - User Profiles
    responses:
      200:
        description: User profiles fetched successfuly
      500:
        description: Internal server error
    """
    user_id=get_jwt_identity()
    profiles=get_user_profiles(user_id)
    return api_response(
        status_code=200,
        message='User profiles fetched successfuly',
        data=profiles,   
    )

@profiles_bp.route("/lessor",methods=['POST'])
@jwt_required(locations=['headers','cookies'])
def create_lessor_profile():
    """
    Create lessor profile
    ---
    description: Add a lessor profile to user
    tags:
      - User Profiles
    consumes:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        schema:
          $ref: '#/definitions/CreateLessorProfile'
    responses:
      201:
        description: Lessor profile created successfuly
      400:
        description: Bad request
      
    """
    user_id=get_jwt_identity()
    create_data=CreateLessorProfileSchema().load(request.get_json())
    profile=add_lessor_profile(user_id=user_id,data=create_data)
    return  api_response(
        status_code=201,
        message='Lessor profile created successfuly',
        data=profile,   
    )

@profiles_bp.route('/<profile_uuid>',methods=['PUT','PATCH'])
@jwt_required(locations=['headers','cookies'])
def update_user_lessor_profile(profile_uuid:str):
    """
    Update  profile 
    ---
    description: update lessor profile
    tags:
      - User Profiles
    consumes:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        schema:
          $ref: '#/definitions/UpdateLessorProfile'
    """
    user_id=get_jwt_identity()
    update_data= UpdateProfileSchema().load(request.get_json() or {})
    profile=update_lessor_profile(user_id=user_id,profile_id=profile_uuid,data=update_data)
    return api_response(
        status_code=200,
        message='Lessor profile updated successfuly',
        data=profile,   
    )
@profiles_bp.route('/<profile_uuid>/status',methods=['PUT'])
@jwt_required(locations=['headers','cookies'])
def update_user_lessor_profile_status(profile_uuid:str):
    """
    Update lessor profile status
    ---
    description: Update a lessor profile status
    tags:
      - User Profiles
    consumes:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        schema:
          $ref: '#/definitions/UpdateLessorProfileStatus'
    """
    user_id=get_jwt_identity()
    update_data= UpdateProfileSchemaStatus().load(request.get_json() or {})
    profile=update_lessor_profile_status(user_id=user_id,profile_id=profile_uuid,data=update_data)
    return api_response(
        status_code=200,
        message='Lessor profile status updated successfuly',
        data=profile,   
    )

    

