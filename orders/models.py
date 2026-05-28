from extensions import db
from utils.BaseModel import BaseModel
from uuid import uuid4
from enum import Enum

class OrderStatus(Enum):
    PENDING='pending'
    CONFIRMED='confirmed'
    SHIPPED='shipped'
    DELIVERED='delivered'
    CANCELLED='cancelled'

class OrderItem(BaseModel):
    __tablename__='order_items'
    id=db.Column(db.Integer,primary_key=True)
    uuid=db.Column(db.UUID(as_uuid=True),default=uuid4,unique=True)
    quantity=db.Column(db.Integer,nullable=False)
    price=db.Column(db.Float,nullable=False)

    order_id=db.Column(db.Integer,db.ForeignKey('orders.id'),nullable=False)
    listing_id=db.Column(db.Integer,db.ForeignKey('listings.id'),nullable=False)

    #relations
    order=db.relationship('Order',back_populates='items')
    listing=db.relationship('Listing')

class Order (BaseModel):
    __tablename__='orders'
    id=db.Column(db.Integer,primary_key=True)
    uuid=db.Column(db.UUID(as_uuid=True),default=uuid4,unique=True)
    status=db.Column(db.String(50),default=OrderStatus.PENDING,nullable=False)
    total_amount=db.Column(db.Float,nullable=False)

    items=db.relationship('OrderItem',back_populates='order',cascade='all, delete-orphan')
    payment=db.relationship('Payment',back_populates='order', uselist=False, cascade='all, delete-orphan')
    
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
        unique=True
    )
    user=db.relationship(
        "User",
        back_populates='orders',
    )