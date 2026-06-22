from flask import Blueprint
from users.services import getAllUsers,get_current_user
from utils.response import api_response
from flask_jwt_extended import jwt_required, get_jwt_identity

users_bp=Blueprint('users',__name__)

@users_bp.route('/',methods=['GET'])
def getAll():
    users=getAllUsers()
    return api_response(
        message="User fetched successfuly",
        data=users,
        status_code=200
    )

@users_bp.route('/me',methods=['GET'])
@jwt_required(locations=['headers','cookies'])
def getMe():
    print('here')
    user_id=get_jwt_identity()
    user=get_current_user(user_id=user_id)
    return api_response(
        message="User details fetched successfuly",
        data=user,
        status_code=200
    )
