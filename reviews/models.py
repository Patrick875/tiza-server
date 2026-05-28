from extensions import db
from utils.BaseModel import BaseModel
from uuid import uuid4

class Review(BaseModel):
    __tablename__='reviews'
    id=db.Column(db.Integer,primary_key=True)
    uuid=db.Column(db.UUID(as_uuid=True),default=uuid4,unique=True)
    rating=db.Column(db.Integer,nullable=False)
    comment=db.Column(db.String())
    reviewer_id=db.Column(db.Integer,db.ForeignKey('users.id'),nullable=False)
    listing_id=db.Column(db.Integer,db.ForeignKey('listings.id'),nullable=False)

    #relations
    reviewer=db.relationship('User',back_populates='reviews')
    listing=db.relationship('Listing',back_populates='reviews')