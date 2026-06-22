from extensions import db
from database.BaseModel import BaseModel
from uuid import uuid4


class CartItem(BaseModel):
    __tablename__='cart_items'
   
    quantity=db.Column(db.Integer,default=1)
    price=db.Column(db.Float,nullable=False)

    #relations
    cart_id=db.Column(db.Integer,db.ForeignKey('carts.id'),nullable=False)
    cart=db.relationship('Cart',back_populates='items')

    listing_id=db.Column(db.Integer,db.ForeignKey('listings.id'),nullable=False)
    listing=db.relationship('Listing')

class Cart (BaseModel):
    __tablename__='carts'
   
    #other props
    total_amount=db.Column(db.Float,default=0.0)
    total_items=db.Column(db.Integer,default=0)

    #relations
    items=db.relationship('CartItem',back_populates='cart',cascade='all, delete-orphan')
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
        unique=True
    )
    user=db.relationship(
        "User",
        back_populates='cart',
    )