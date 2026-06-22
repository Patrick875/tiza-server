from app import create_app
from extensions import db
from auth.models import Role,role_permissions,Permission


ROLES_PERMISSIONS = {
    'renter': {
        'display_name': 'Renter',
        'description': 'User who rents items from others',
        'permissions': [
            # Browsing & Discovery
            'browse_listings',
            'search_listings',
            'view_listing_details',
            'filter_listings',
            
            # Cart & Checkout
            'add_to_cart',
            'view_cart',
            'remove_from_cart',
            'update_cart',
            'checkout',
            'create_booking',
            
            # Rentals Management
            'view_own_rentals',
            'view_rental_details',
            'initiate_return',
            'view_return_status',
            
            # Reviews & Ratings
            'leave_review',
            'view_own_reviews',
            'edit_own_review',
            'delete_own_review',
            
            # Messaging
            'message_lessor',
            'view_messages',
            
            # Profile
            'view_own_profile',
            'edit_own_profile',
            'change_password',
            'view_notification_settings',
            'edit_notification_settings',
            
            # Support
            'view_faq',
            'contact_support',
            'view_support_tickets',
        ]
    },
    
    'lessor': {
        'display_name': 'Lessor',
        'description': 'User who leases items to others',
        'permissions': [
            # All renter permissions (lessor can also rent)
            'browse_listings',
            'search_listings',
            'view_listing_details',
            'filter_listings',
            'add_to_cart',
            'view_cart',
            'remove_from_cart',
            'update_cart',
            'checkout',
            'create_booking',
            'view_own_rentals',
            'view_rental_details',
            'initiate_return',
            'view_return_status',
            'leave_review',
            'view_own_reviews',
            'edit_own_review',
            'delete_own_review',
            'message_lessor',
            'view_messages',
            'view_own_profile',
            'edit_own_profile',
            'change_password',
            'view_notification_settings',
            'edit_notification_settings',
            'view_faq',
            'contact_support',
            'view_support_tickets',
            
            # Lessor-specific: Listings
            'create_listing',
            'view_own_listings',
            'edit_own_listing',
            'delete_own_listing',
            'archive_listing',
            'upload_listing_photos',
            'set_listing_pricing',
            'set_listing_inclusions',
            'set_damage_policy',
            'view_listing_stats',
            
            # Lessor-specific: Incoming Rentals
            'view_incoming_bookings',
            'view_incoming_booking_details',
            'message_renter',
            'confirm_item_return',
            'check_return_condition',
            
            # Lessor-specific: Returns & Damage
            'view_return_requests',
            'submit_damage_claim',
            'view_damage_claims',
            'edit_damage_claim',
            'respond_to_dispute',
            
            # Lessor-specific: Earnings
            'view_earnings',
            'view_payment_history',
            'update_payout_method',
            'view_transaction_history',
            
            # Lessor-specific: Reviews
            'view_lessor_reviews',
            'respond_to_review',
            
            # Lessor-specific: Settings
            'edit_lessor_profile',
            'update_lessor_settings',
            'view_lessor_verification_status',
        ]
    },
    
    'admin': {
        'display_name': 'Administrator',
        'description': 'Platform administrator with full access',
        'permissions': [
            # All lessor permissions (admins can do everything lessors can)
            'browse_listings',
            'search_listings',
            'view_listing_details',
            'filter_listings',
            'add_to_cart',
            'view_cart',
            'remove_from_cart',
            'update_cart',
            'checkout',
            'create_booking',
            'view_own_rentals',
            'view_rental_details',
            'initiate_return',
            'view_return_status',
            'leave_review',
            'view_own_reviews',
            'edit_own_review',
            'delete_own_review',
            'message_lessor',
            'view_messages',
            'view_own_profile',
            'edit_own_profile',
            'change_password',
            'view_notification_settings',
            'edit_notification_settings',
            'view_faq',
            'contact_support',
            'view_support_tickets',
            'create_listing',
            'view_own_listings',
            'edit_own_listing',
            'delete_own_listing',
            'archive_listing',
            'upload_listing_photos',
            'set_listing_pricing',
            'set_listing_inclusions',
            'set_damage_policy',
            'view_listing_stats',
            'view_incoming_bookings',
            'view_incoming_booking_details',
            'message_renter',
            'confirm_item_return',
            'check_return_condition',
            'view_return_requests',
            'submit_damage_claim',
            'view_damage_claims',
            'edit_damage_claim',
            'respond_to_dispute',
            'view_earnings',
            'view_payment_history',
            'update_payout_method',
            'view_transaction_history',
            'view_lessor_reviews',
            'respond_to_review',
            'edit_lessor_profile',
            'update_lessor_settings',
            'view_lessor_verification_status',
            
            # Admin-specific: User Management
            'manage_all_users',
            'view_all_users',
            'view_user_details',
            'suspend_user',
            'unsuspend_user',
            'delete_user',
            'message_user',
            'verify_user_identity',
            
            # Admin-specific: Listings Management
            'manage_all_listings',
            'view_all_listings',
            'approve_listing',
            'reject_listing',
            'remove_listing',
            'flag_listing_for_review',
            'delist_listing',
            'edit_any_listing',
            
            # Admin-specific: Bookings & Orders
            'manage_all_bookings',
            'view_all_bookings',
            'view_booking_details',
            'cancel_booking',
            'issue_refund',
            
            # Admin-specific: Disputes & Issues
            'manage_disputes',
            'view_all_disputes',
            'view_dispute_details',
            'resolve_dispute',
            'make_dispute_decision',
            'view_damage_claims_all',
            'approve_damage_claim',
            'reject_damage_claim',
            'view_return_issues',
            'resolve_return_issue',
            
            # Admin-specific: Payments & Transactions
            'manage_payments',
            'view_all_payments',
            'view_all_transactions',
            'view_refund_logs',
            'process_refund',
            'view_payment_analytics',
            'view_platform_commission',
            
            # Admin-specific: Reports & Analytics
            'view_analytics',
            'view_platform_stats',
            'view_user_growth',
            'view_revenue_reports',
            'view_popular_listings',
            'view_top_lessors',
            'export_reports',
            
            # Admin-specific: Content Management
            'manage_categories',
            'create_category',
            'edit_category',
            'delete_category',
            'manage_category_inclusions',
            'manage_static_pages',
            'edit_faq',
            'manage_banners',
            'manage_featured_listings',
            
            # Admin-specific: Platform Settings
            'manage_platform_settings',
            'view_platform_settings',
            'update_commission_rate',
            'update_fee_structure',
            'update_refund_policies',
            'manage_feature_flags',
            'update_email_templates',
            'update_sms_settings',
            
            # Admin-specific: Verification & Moderation
            'manage_verification',
            'view_pending_verifications',
            'approve_verification',
            'reject_verification',
            'manage_flagged_content',
            'view_flagged_listings',
            'view_flagged_users',
            'review_flagged_content',
            
            # Admin-specific: Support & Tickets
            'manage_support_tickets',
            'view_all_tickets',
            'assign_ticket',
            'respond_to_ticket',
            'close_ticket',
            
            # Admin-specific: Logs & Monitoring
            'view_logs',
            'view_api_logs',
            'view_error_logs',
            'view_activity_logs',
            'view_security_events',
            'view_system_health',
        ]
    }
}

app= create_app

def seed_roles_permissions():
    """
    Seed all roles and permissions into the database.
    Run this once during initial setup.
    """
    for role_name, role_data in ROLES_PERMISSIONS.items():
        existing_role= Role.query.filter_by(name=role_name).first()
        if existing_role:
            print(f"Role '{role_name}' already exists. Skipping...")
            continue
        role=Role(
            name=role_name,
            display_name=role_data["display_name"],
            description=role_data['description']
        )
        db.session.add(role)
        db.session.flush()

        for permission_name in role_data['permissions']:
            permission= Permission.query.filter_by(name=permission_name).first()
            if not permission:
                permission=Permission(name=permission_name)
                db.session.add(permission)
                db.session.flush()
            
            if permission not in role.permissions:
                role.permissions.append(permission)
        
        print(f"✓ Role '{role_name}' created with {len(role_data['permissions'])} permissions")

        db.session.commit()
        print("✓ Roles and permissions seeded successfully!")

if __name__=="__main__":
    seed_roles_permissions()
