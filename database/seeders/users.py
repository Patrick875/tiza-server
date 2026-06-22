from users.models import User,UserStatus
from auth.models import Role
from profiles.models import Profile
from app import create_app
from werkzeug.security import generate_password_hash
from extensions import db


app=create_app()

def seed_admin_user():
    """
    Seed initial admin user with profile
    Run this once during initial setup
    """
    with app.app_context():

        admin_email="admin@rentalmarketplace.com"
        admin_password="AdminPassword123!"
        existing_admin= User.query.filter_by(email=admin_email).first()
        if existing_admin:
            print(f"✗ Admin user with email '{admin_email}' already exists. Skipping...")
            return
        
        try:
            admin_role= Role.query.filter_by(name='admin').first()
            if not admin_role:
                print("✗ Admin role does not exist. Run 'seed_roles_and_permissions' first!")
                return
            admin_user=User(
                email=admin_email,
                password_hash=generate_password_hash(admin_password),
                first_name='Admin',
                last_name='User',
                phone='+1234567890',
                email_verified=True,
                status=UserStatus.ACTIVE.value
            )
            admin_user.roles.append(admin_role)
            db.session.add(admin_user)
            db.session.flush()


            admin_profile=Profile(
                user_id=admin_user.id,
                bio='Platform Administrator',
                location='Headquarters',
                profile_picture=None,
                theme='light',
                whatsapp=None,
                telegram=None,
                twitter=None,
                instagram=None,
                facebook=None
            )
            db.session.add(admin_profile)
            db.session.commit()
            print(f"""
                ✓ Admin user created successfully!
                Email: {admin_email}
                Password: {admin_password}
                Role: admin
                Status: ACTIVE
    
    ⚠️          IMPORTANT: Change the admin password immediately in production!
                """
            )
        except Exception as e:
            db.session.rollback()
            print(f"✗ Error seeding admin user: {str(e)}")

if __name__=="__main__":
    seed_admin_user()