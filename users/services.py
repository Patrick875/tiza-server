from flask import jsonify
from users.models import User


def getAllUsers():
    data=User.query.all()
    # print(f'users {data}')
    return jsonify(data)