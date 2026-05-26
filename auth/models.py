from extensions import db
from utils.BaseModel import BaseModel
from uuid import uuid4

#associations
user_roles=db.Table(
     'user_roles',
    db.Column("user_id", db.Integer, db.ForeignKey("users.id"), primary_key=True),
    db.Column("role_id", db.Integer, db.ForeignKey("roles.id"), primary_key=True)
)
role_permissions = db.Table(
    "role_permissions",
    db.Column("role_id", db.Integer, db.ForeignKey("roles.id"), primary_key=True),
    db.Column("permission_id", db.Integer, db.ForeignKey("permissions.id"), primary_key=True),
)


class Role(BaseModel):
    __tablename__='roles'
    
    id=db.Column(db.Integer,primary_key=True,nullable=False)
    uuid=db.Column(db.UUID(as_uuid=True),unique=True,default=uuid4)
    name=db.Column(db.String(100),unique=True,nullable=False)

    #relationships
    users=db.relationship(
        'User',
        secondary=user_roles,
        back_populates='roles'
    )
    permissions=db.relationship(
        'Permission',
        secondary=role_permissions,
        back_populates='roles'
    )


class Permission(BaseModel):
     __tablename__='permissions'
     id=db.Column(db.Integer,primary_key=True,nullable=False)
     uuid=db.Column(db.UUID(as_uuid=True),unique=True,default=uuid4)
     name=db.Column(db.String(100),unique=True,nullable=False)
 
     #relationships
     roles=db.relationship(
         'Role',
         secondary=role_permissions,
         back_populates='permissions'
     )
