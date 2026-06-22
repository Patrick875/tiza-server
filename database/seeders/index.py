from database.seeders.rbac import seed_roles_permissions
from database.seeders.users import seed_admin_user
def run_seeders():
    seed_roles_permissions()
    seed_admin_user()

if __name__=='__main__':
    seed_roles_permissions()