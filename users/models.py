from extensions import db
from utils.BaseModel import BaseModel
from uuid import uuid4
from auth.models import user_roles
from enum import Enum

class UserStatus(Enum):
    PENDING_EMAIL_VERIFICATION='PENDING_EMAIL_VERIFICATION'
    ACTIVE='ACTIVE'
    INACTIVE='INACTIVE'
    DELETED='DELETED'

class User (BaseModel):
    __tablename__='users'
    id=db.Column(db.Integer,primary_key=True)
    uuid=db.Column(db.UUID(as_uuid=True),default=uuid4,unique=True)

    email=db.Column(db.String(255),unique=True,nullable=False)
    password_hash=db.Column(db.String(255),nullable=False)

    first_name=db.Column(db.String())
    last_name=db.Column(db.String())
    phone=db.Column(db.String(),nullable=True)

    email_verified=db.Column(db.Boolean,default=False)
    status=db.Column(db.Enum(UserStatus),default=UserStatus.PENDING_EMAIL_VERIFICATION)

    #relations

    roles=db.relationship(
        'Role',
        secondary=user_roles,
        back_populates='users',
    )

    profile=db.relationship(
        'Profile',
        back_populates='user',
        uselist=False,
        cascade='all,delete-orphan'
        )
    listings=db.relationship(
        "Listing",
        back_populates='user',
        cascade='all,delete-orphan'
    )
    rentals=db.relationship(
        "Rental",
        back_populates='user',
        cascade='all,delete-orphan'
    )
    orders=db.relationship(
        "Order",
        back_populates='user',
        cascade='all,delete-orphan'
    )
    cart=db.relationship(
        'Cart',
        back_populates='user',
        uselist=False,
        cascade='all,delete-orphan'
    )


