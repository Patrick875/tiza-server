from extensions import db
from database.BaseModel import BaseModel
from uuid import uuid4

class Profile (BaseModel):
    __tablename__='profiles'
   
    bio=db.Column(db.String(500))
    location=db.Column(db.String(255))
    website=db.Column(db.String(255))
    profile_picture=db.Column(db.String(500))
    theme=db.Column(db.String(50),default="light")
    whatsapp=db.Column(db.String(20))
    telegram=db.Column(db.String(20))
    twitter=db.Column(db.String(20))
    instagram=db.Column(db.String(20))
    facebook=db.Column(db.String(20))

    #other props

    #relations

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
        unique=True
    )
    user=db.relationship(
        "User",
        back_populates='profile',
    )