from extensions import db
from utils.BaseModel import BaseModel
from uuid import uuid4

class Rental (BaseModel):
    __tablename__='rentals'
    id=db.Column(db.Integer,primary_key=True)
    uuid=db.Column(db.UUID(as_uuid=True),default=uuid4,unique=True)

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
        back_populates='rentals'
    )