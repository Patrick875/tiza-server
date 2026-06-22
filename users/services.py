from flask import jsonify
from users.models import User


def getAllUsers():
    data=User.query.all()
    # print(f'users {data}')
    return jsonify(data)

def get_current_user(user_id:int):
    user= User.query.filter_by(id=user_id).first()
    if not user:
        raise ValueError("User not found")
    return user.to_dict()