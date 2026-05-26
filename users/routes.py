from flask import Blueprint
from users.services import getAllUsers
from utils.response import api_response

users_bp=Blueprint('users',__name__)

@users_bp.route('/',methods=['GET'])
def getAll():
    users=getAllUsers()
    return api_response(
        message="User fetched successfuly",
        data=users,
        status_code=200
    )
