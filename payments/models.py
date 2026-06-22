from extensions import db
from extensions import db
from database.BaseModel import BaseModel
from uuid import uuid4
from enum import Enum


class PaymentStatus(Enum):
    PENDING='pending'
    COMPLETED='completed'
    FAILED='failed'
    REFUNDED='refunded'

class Payment(BaseModel):
    __tablename__='payments'
    
    amount=db.Column(db.Float,nullable=False)
    status=db.Column(db.String(50),default=PaymentStatus.PENDING.value,nullable=False)
    order_id=db.Column(db.Integer,db.ForeignKey('orders.id'),nullable=False)

    #relations
    order=db.relationship('Order',back_populates='payment')
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
        unique=True
    )
    user=db.relationship(
        "User",
        back_populates='payments',
    )
