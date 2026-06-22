from extensions import db
from database.BaseModel import BaseModel
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
    name=db.Column(db.String(100),unique=True,nullable=False)
    display_name=db.Column(db.String(100),unique=True)
    description=db.Column(db.String(100))
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
    def has_permission(self, permission_name):
         return any(p.name==permission_name for p in self.permissions)
    def __repr__(self):
        return f'<Role {self.name}>'

class Permission(BaseModel):
     __tablename__='permissions'
     name=db.Column(db.String(100),unique=True,nullable=False)
     #relationships
     roles=db.relationship(
         'Role',
         secondary=role_permissions,
         back_populates='permissions'
     )
