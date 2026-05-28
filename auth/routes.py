from flask import Blueprint,request,url_for
from marshmallow import ValidationError
from auth.shemas import SignupSchema,LoginSchema
from auth.services import signup,login_user,generate_verification_token,verify_user_email
from utils.response import api_response
from flask_jwt_extended import set_refresh_cookies,jwt_required,create_access_token,get_jwt_identity
from datetime import timedelta
from users.models import User
from utils.EmailService import send_email
auth_bp=Blueprint('auth',__name__)

@auth_bp.route('/register',methods=['POST'])
def register():
    try:
        data= SignupSchema().load(request.get_json() or {})
        user=signup(data)
        token=generate_verification_token(user["id"])
        verify_url = url_for(
            "auth.verify_email",
            token=token,
            _external=True
        )
        send_email(
            subject="Verify your email",
            email_template="verify_email",
            recipients=[user["email"]],
            values={
                "name": user["first_name"] + " " + user["last_name"],
                "verify_url": verify_url
            }
        )

        return api_response(
            message="User registered successfully",
            data=user,
            status_code=201
        )
    except ValidationError as error:
        return api_response(
            success=False,
            message="Validation failed",
            errors=error.messages,
            status_code=400
        )
        
@auth_bp.route('/login',methods=['POST'])
def login():
    try:
        data= LoginSchema().load(request.get_json())
        tokens=login_user(data)
        response=api_response(
            success=True,
            data={
                "access_token":tokens["access_token"],
                "user":tokens["user"]
            },
            status_code=200,
            message="Login successful"
            )
        set_refresh_cookies(response,tokens["refresh_token"])
        return response

    except ValidationError as error:
        return api_response(
            success=False,
            errors=error.messages,
            status_code=400)
    except ValueError as error:
        return api_response(
            success=False,
            message=str(error),
            status_code=400,
        )
    
@auth_bp.route('/refresh-token',methods=['POST'])
@jwt_required(refresh=True,locations=['cookies'])
def refresh_token():
    user_id=get_jwt_identity()
    user=User.query.filter_by(id=user_id).first()
    if not user:
         return api_response(
            success=False,
            message="Invalid credentials please login again",
            status_code=401,
        )
    access_token=create_access_token(
        identity=str(user_id),
        additional_claims={
            "email":user.email,
            "roles":[role.name for role in user.roles] or []
        },
        expires_delta=timedelta(minutes=15)
        )
    return api_response(
        success=True,
        message="Token refreshed",
        data={"access_token": access_token},
    )


@auth_bp.route('/verify/<token>',methods=['GET'])
def verify_email(token):
   return verify_user_email(token)
    

# @auth_bp.route('/reset-password',methods=['POST'])
# def register():
#     data= request.get_json()
#     print('user-register-route')
#     return jsonify({
#         "message":'User registered',
#         "data":{"user-id":123}
#     }),201