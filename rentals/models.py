from extensions import db
from database.BaseModel import BaseModel
from uuid import uuid4

class Rental (BaseModel):
    __tablename__='rentals'
   
    #relations
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
        unique=True
    )
    user=db.relationship(
        "User",
        back_populates='rentals'
    )