from extensions import db
from uuid import uuid4
from database.BaseModel import BaseModel
from listings.models import LeaseType
from enum import Enum

class PriceStatus(Enum):
    ACTIVE='ACTIVE'
    INACTIVE='INACTIVE'
    ARCHIVED='ARCHIVED'
    DELETED='DELETED'

class Price(BaseModel):
    __tablename__='prices'

    lease_duration=db.Column(db.Integer,nullable=False)
    lease_type=db.Column(db.String(50), default=LeaseType.DAY.value,nullable=False)
    amount=db.Column(db.Float,nullable=False)
    listing_id=db.Column(db.Integer,db.ForeignKey('listings.id'),nullable=False)
    status=db.Column(db.String(50),default=PriceStatus.ACTIVE.value)

    #relations
    listing=db.relationship('Listing',back_populates='prices')

    def to_dict(self):
        return {
            "id":str(self.uuid),
            "lease_duration":self.lease_duration,
            "lease_type":self.lease_type,
            "status":self.status,
            "amount":self.amount,
            "created_at":self.created_at.isoformat(),
            "updated_at":self.updated_at.isoformat()
        }
