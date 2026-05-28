from extensions import db
from utils.BaseModel import BaseModel
from uuid import uuid4
from enum import Enum
from sqlalchemy.dialects.postgresql import ARRAY

class ListingCondition(Enum):
    NEW="NEW"
    LIKE_NEW="LIKE_NEW" 
    GOOD="GOOD" 
    FAIR="FAIR"
class ListingVerification(Enum):
    VERIFIED="VERIFIED"
    PENDING="PENDING" 
    CANCELED="CANCELED" 

class LeaseType(Enum):
    HOUR='HOUR' 
    DAY='DAY' 
    WEEK='WEEK' 
    MONTH='MONTH'
class ListingStatus(Enum):
    AVAILABLE='AVAILABLE' 
    RENTED='RENTED' 
class CancelationPolicy(Enum):
    FLEXIBLE="FLEXIBLE" 
    MODERATE="MODERATE"  
    STRICT="STRICT"

class Listing (BaseModel):
    __tablename__='listings'

    id=db.Column(db.Integer,primary_key=True)
    uuid=db.Column(db.UUID(as_uuid=True),default=uuid4,unique=True)
    name=db.Column(db.String(255),nullable=False)
    description=db.Column(db.String())
    listing_verification=db.Column(db.String(),default=ListingVerification.PENDING.value)
    condition=db.Column(db.String(50),default=ListingCondition.GOOD.value)
    tags=db.Column(ARRAY(db.String),default=list)
    included_items=db.Column(db.JSON,default=list)
    leasing_types = db.Column(
        ARRAY(db.String(50)),
        default=list,
        nullable=False)
    primary_lease_type=db.Column(db.String(50),nullable=False)
    security_deposit=db.Column(db.Integer(),default=0)
    status= db.Column(db.String(50),default=ListingStatus.AVAILABLE.value)
    available_from=db.Column(db.DateTime,nullable=True)
    available_to=db.Column(db.DateTime,nullable=True)
    minimum_rental_period=db.Column(db.Integer())
    maximum_rental_period=db.Column(db.Integer())
    delivery_available= db.Column(db.BOOLEAN);
    delivery_fee=db.Column(db.Integer())
    rating=db.Column(db.Float())

    cancellation_policy=db.Column(db.String(),default=CancelationPolicy.FLEXIBLE.value)
    contract=db.Column(db.JSON,nullable=True)
    #other props

    #relations
    prices=db.relationship('Price',back_populates='listing',cascade='all, delete-orphan')

    category_id=db.Column(db.Integer,db.ForeignKey('categories.id'),nullable=False)
    category=db.relationship(
        "Category",
        back_populates="listings"
    )
    lessor_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
    )
    lessor=db.relationship(
        "User",
        back_populates='listings',
    )

    reviews=db.relationship('Review',back_populates='listing',cascade='all, delete-orphan')
    review_count=db.Column(db.Integer(),default=0)
    review_count = db.Column(db.Integer, default=0)
    view_count = db.Column(db.Integer, default=0)
    favorite_count = db.Column(db.Integer, default=0)
    share_count = db.Column(db.Integer, default=0)
    chat_count = db.Column(db.Integer, default=0)


    def to_dict(self):
       return {
           "id":str(self.uuid),
           "name":self.name,
           "description":self.description,
           "prices":[price.to_dict() for price in self.prices],
           "listing_verification":self.listing_verification,
           "condition":self.condition,
           "tags":self.tags,
           "included_items":self.included_items,
           "leasing_types":self.leasing_types,
           "primary_lease_type":self.primary_lease_type,
           "security_deposit":self.security_deposit,
           "status":self.status,
           "available_from":self.available_from.isoformat() if self.available_from else None,
           "available_to":self.available_to.isoformat() if self.available_to else None,
           "minimum_rental_period":self.minimum_rental_period,
           "maximum_rental_period":self.maximum_rental_period,
           "delivery_available":self.delivery_available,
           "delivery_fee":self.delivery_fee,
           "rating":self.rating,
           "cancellation_policy":self.cancellation_policy,
           "category":{"id":self.category.id,"name":self.category.name} if self.category else None,
           "lessor":{"id":self.lessor.id,"first_name":self.lessor.first_name,"last_name":self.lessor.last_name,"email":self.lessor.email} if self.lessor else None,
           "review_count":self.review_count,
           "view_count":self.view_count,
           "favorite_count":self.favorite_count,
           "share_count":self.share_count,
           "chat_count":self.chat_count,
           'created_at':self.created_at.isoformat(),
           'updated_at':self.updated_at.isoformat(),
       }
    
    def to_list_item(self):
        return {
            "id":str(self.uuid),
            "name":self.name,
            "category":{"id":self.category.id,"name":self.category.name} if self.category else None,
            "primary_lease_type":self.primary_lease_type,
            "location":self.lessor.profile.location if self.lessor and self.lessor.profile else None,
            "rating":self.rating,
            "status":self.status,
            "price":self.prices[0].amount if self.prices else None,
            "leasingType":self.prices[0].lease_type if self.prices else None,
            "createdAt":self.created_at.isoformat(),
            "updatedAt":self.updated_at.isoformat(),
        }
    def update_review_count(self):
        self.review_count = len(self.reviews)
    
    def update_rating(self):
        if self.reviews:
            total_rating = sum(review.rating for review in self.reviews)
            self.rating = total_rating / len(self.reviews)
        else:
            self.rating = 0.0
        