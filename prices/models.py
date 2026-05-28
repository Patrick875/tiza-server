from extensions import db
from uuid import uuid4
from utils.BaseModel import BaseModel
from listings.models import LeaseType
class Price(BaseModel):
    __tablename__='prices'
    id=db.Column(db.Integer,primary_key=True)
    uuid=db.Column(db.UUID(as_uuid=True),default=uuid4,unique=True)
    lease_duration=db.Column(db.Integer,nullable=False)
    lease_type=db.Column(db.String(50), default=LeaseType.DAY.value,nullable=False)
    amount=db.Column(db.Float,nullable=False)
    listing_id=db.Column(db.Integer,db.ForeignKey('listings.id'),nullable=False)

    #relations
    listing=db.relationship('Listing',back_populates='prices')

    def to_dict(self):
        return {
            "id":str(self.uuid),
            "lease_duration":self.lease_duration,
            "lease_type":self.lease_type,
            "amount":self.amount,
            "created_at":self.created_at,
            "updated_at":self.updated_at
        }
