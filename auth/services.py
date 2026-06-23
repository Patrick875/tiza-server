from extensions import db
from werkzeug.security import generate_password_hash,check_password_hash
from werkzeug.exceptions import NotFound,BadRequest
from flask_jwt_extended import create_access_token,create_refresh_token
from datetime import timedelta
from users.models import User,UserStatus
from auth.models import Role
from profiles.models import Profile
from itsdangerous import URLSafeTimedSerializer
from flask import current_app
from utils.response import api_response

def generate_tokens(user):
    access_token=create_access_token(
        identity=str(user.id),
        additional_claims={
            "email":user.email,
            "roles":[role.name for role in user.roles] or [],
        },
        expires_delta=timedelta(minutes=15)
    )
    refresh_token=create_refresh_token(identity=str(user.id))
    return {
        "access_token":access_token,
        "refresh_token":refresh_token,
        "user":{
            "id":user.uuid,
            "email":user.email,
            "full_name":f"{user.first_name} {user.last_name}",
            "status":user.status
        }
    }

def generate_verification_token(user_id:int):
    serializer=URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return serializer.dumps({"user_id":user_id},salt=current_app.config['EMAIL_VERIFICATION_SALT'])

def verify_verification_token(token:str,max_age=3600*4):
    serializer = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
    data = serializer.loads(
            token,
            salt=current_app.config['EMAIL_VERIFICATION_SALT'],
            max_age=max_age
        )
    return data["user_id"]
  
def signup(data):
    alread_exists= User.query.filter_by(email=data['email']).first();

    if alread_exists:
        raise BadRequest('Email already exists')
    
    user=User(
        email=data['email'],
        password_hash=generate_password_hash(data['password']),
        first_name=data["first_name"],
        last_name=data["last_name"],
        phone=data.get("phone"),
        status=UserStatus.ACTIVE.value
    )
    renter_role= Role.query.filter_by(name='renter').first()
    user.roles.append(renter_role)

    db.session.add(user)
    db.session.commit()

    return {
        "id":user.id,
        'uuid':str(user.uuid),
        'email':user.email,
        'first_name':user.first_name,
        'last_name':user.last_name
    }

def login_user (data):
    email= data['email']
    password=data['password']

    db_user=User.query.filter_by(email=email).filter(User.status.in_([item.value for item in UserStatus])).first()
    if not db_user:
        raise BadRequest("Invalid email or password")
    elif db_user.status==UserStatus.PENDING_EMAIL_VERIFICATION.value:
        raise BadRequest("User account not verified please verify you account to login")
    db_password=db_user.password_hash
    
    if not check_password_hash(db_password,password):
        raise BadRequest("Wrong email or password, Please try again")
    return generate_tokens(db_user)


def verify_user_email(token: str):
    user_id = verify_verification_token(token)

    if not user_id:
        return api_response(
            success=False,
            message="Invalid or expired verification link",
            status_code=400
        )
    
    try:
        user = User.query.filter_by(id=user_id).first()
        profile=Profile(
            bio='',
            location="",
            website="",
            profile_picture="",
            theme="",
            whatsapp="",
            telegram="",
            twitter="",
            instagram="",
            facebook="",
            user_id=user_id
        )

        db.session.add(profile)
        db.session.commit()

        if not user:
            raise NotFound("User not found")

        if user.email_verified:
            return api_response(
                success=True,
                message="Email already verified",
                status_code=200
            )

        user.email_verified = True
        user.status = UserStatus.ACTIVE.value

        db.session.commit()

        return api_response(
            success=True,
            message="Email verified successfully",
            status_code=200
        )
    except Exception as e:
        print(f""" 
                {str(e)}
            """)
        raise ValueError(str(e))

    