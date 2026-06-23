from profiles.models import RentorProfile,LessorProfile,Profile
from users.models import User
from auth.models import Role
from extensions import db
from werkzeug.exceptions import NotFound,BadRequest,Unauthorized

def get_user_profiles(user_id):
    rentor_profile=RentorProfile.query.filter_by(user_id=user_id).first()
    lessor_profile=LessorProfile.query.filter_by(user_id=user_id).first()
    user_profile=Profile.query.filter_by(user_id=user_id).first()

    return {
        "rentor_profile":rentor_profile.to_dict() if rentor_profile else None,
        "lessor_profile":lessor_profile.to_dict() if lessor_profile else None,
        "generic_profile":user_profile.to_dict() if user_profile else None,
    }

def add_lessor_profile(user_id:int,data:dict):
    try:
        user=User.query.filter_by(id=user_id).first()

        if not user:
            raise NotFound("User not found")
        lessor_role= Role.query.filter_by(name='lessor').first()

        if not lessor_role:
            raise NotFound('Lessor role not found')
        
        if lessor_role:
            user.roles.append(lessor_role)
        
        lessor_profile=LessorProfile(
            user_id=user_id,
            display_name = data.get("display_name",""),
            business_type = data.get("business_type",""),
            verification_status = data.get("verification_status",""),
            preferred_listing_categories = data.get("preferred_listing_categories",""),
            payout_phone = data.get("payout_phone",""),
            payout_bank_name = data.get("payout_bank_name",""),
            payout_account_number = data.get("payout_account_number",""),
            total_listings = data.get("total_listings",0)  
        )
        db.session.add(lessor_profile)
        db.session.commit()
        return lessor_profile.to_dict()
    except Exception as e:
        print(f""" 
                error adding profile {str(e)}
             """)
        raise 
    
def update_lessor_profile(user_id:int,profile_id:str,data:dict):
    fields = [
        "display_name",
        "business_type",
        "verification_status",
        "preferred_listing_categories",
        "payout_phone",
        "payout_bank_name",
        "payout_account_number",
        "total_listings",
    ]
    try:
        lessor_profile= LessorProfile\
            .query.filter(
                LessorProfile.user_id==user_id,
                LessorProfile.uuid==profile_id )\
                .first()
        if not lessor_profile:
            raise NotFound('Lessor profile not found')
        for field in fields:
            value = data.get(field)
            if value is not None:
                setattr(lessor_profile, field, value)
        db.session.commit()
        
        return lessor_profile.to_dict()
    
    except Exception as e:
        db.session.rollback()
        raise 
    

def update_lessor_profile_status(user_id:int,profile_id:str,data:dict):
    try:
        lessor_profile= LessorProfile.query.filter(
            LessorProfile.user_id==user_id,
            LessorProfile.uuid==profile_id,
            ).first()
        if not lessor_profile:
            raise NotFound("Profile not found")
        
        if data.get("status") is None:
            raise BadRequest("Status is required")
        
        lessor_profile.status=data.get("status")
        db.session.commit()
    except Exception as e:
        print(f"""
                error updating profile status {e}
                """)
        db.session.rollback()
        raise 