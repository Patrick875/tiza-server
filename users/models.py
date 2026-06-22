from extensions import db
from database.BaseModel import BaseModel
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

    email=db.Column(db.String(255),unique=True,nullable=False)
    password_hash=db.Column(db.String(255),nullable=False)

    first_name=db.Column(db.String())
    last_name=db.Column(db.String())
    phone=db.Column(db.String(),nullable=True)

    email_verified=db.Column(db.Boolean,default=False)
    status=db.Column(db.String(50),default=UserStatus.PENDING_EMAIL_VERIFICATION.value)

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
        back_populates='lessor',
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
    reviews=db.relationship(
        'Review',
        back_populates='reviewer',
        cascade='all,delete-orphan'
    )
    payments=db.relationship(
        'Payment',
        back_populates='user',
        cascade='all,delete-orphan'
    )


    def to_dict(self):
        return {
            "id":self.id,
            "email":self.email,
            "first_name":self.first_name,
            "last_name":self.last_name,
            "full_name":f"{self.first_name} {self.last_name}",
            "roles":[role.name for role in self.roles],
            "status":self.status
        }
    
    def has_role(self, role_name):
        return any(r.name==role_name for r in self.roles)
    def has_permission(self, permission_name):
        for role in self.roles:
            if role.has_permission(permission_name):
                True
        return False
    def get_all_permissions(self):
        permissions=set()
        for role in self.roles:
            permissions.update(p.name for p in role.permissions)
            return permissions
    def __repr__(self):
        return f'<User {self.email}>'


