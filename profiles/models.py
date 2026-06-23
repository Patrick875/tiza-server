from extensions import db
from database.BaseModel import BaseModel
from uuid import uuid4

class Profile (BaseModel):
    __tablename__='profiles'
   
    bio=db.Column(db.String(500),default='',nullable=True)
    location=db.Column(db.String(255),default='',nullable=True)
    website=db.Column(db.String(255),default='',nullable=True)
    profile_picture=db.Column(db.String(500),nullable=True)
    theme=db.Column(db.String(50),default="light",nullable=True)
    whatsapp=db.Column(db.String(20),nullable=True)
    telegram=db.Column(db.String(20),nullable=True)
    twitter=db.Column(db.String(20),nullable=True)
    instagram=db.Column(db.String(20),nullable=True)
    facebook=db.Column(db.String(20),nullable=True)

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
    def to_dict(self):
        return {
            "bio":self.bio,
            "location":self.location,
            "website":self.website,
            "profile_picture":self.profile_picture,
            "theme":self.theme,
            "whatsapp":self.whatsapp,
            "telegram":self.telegram,
            "twitter":self.twitter,
            "instagram":self.instagram,
            "facebook":self.facebook
        }

class RentorProfile(BaseModel):
    __tablename__='rentor_profiles'

    preferred_location = db.Column(db.String(255))
    max_budget = db.Column(db.Numeric(12, 2))
    preferred_categories = db.Column(db.JSON) 
    rental_frequency = db.Column(db.String(50))
    trust_score = db.Column(db.Float, default=0)
    trust_scorers=db.Column(db.Integer, default=0)
    
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), unique=True)
    user=db.relationship('User',back_populates="rentor_profile")

    def to_dict(self):
        return {
            "prefered_location":self.preferred_location,
            "max_budget":self.max_budget,
            "prefered_categories":self.preferred_categories,
            "rental_frequency":self.rental_frequency,
            "trust_score":self.trust_score,
            "trust_scorers":self.trust_scorers
        }
    def update_trust_score(self,score:int):
        self.trust_score= (self.trust_score + score)/(self.trust_scorers+1)

class LessorProfile(BaseModel):
    __tablename__='lessor_profiles'

    display_name = db.Column(db.String(120))
    business_type = db.Column(db.String(50))
    verification_status = db.Column(db.String(30), default="pending")
    preferred_listing_categories = db.Column(db.JSON)
    payout_phone = db.Column(db.String(20))
    payout_bank_name = db.Column(db.String(100))
    payout_account_number = db.Column(db.String(100))
    total_listings = db.Column(db.Integer, default=0)
    status=db.Column(db.String(20))

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), unique=True)
    user=db.relationship('User',back_populates="lessor_profile")

    def to_dict(self):
        return {
            "display_name":self.display_name,
            "business_type":self.business_type,
            "verification_status":self.verification_status,
            "preferred_listing_categories":self.preferred_listing_categories,
            "payout_phone":self.payout_phone,
            "payout_bank_name":self.payout_bank_name,
            "payout_account_number":self.payout_account_number,
            "total_listings":self.total_listings,
        }
