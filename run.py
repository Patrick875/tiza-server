from app import create_app
from dotenv import load_dotenv
from database.seeders.rbac import seed_roles_permissions
from database.seeders.users import seed_admin_user
from database.seeders.index import run_seeders
from flask.cli import with_appcontext


import os

load_dotenv()

app = create_app()

#scripts

@app.cli.command('seed-rbac')
@with_appcontext
def seed_rbac():
    seed_roles_permissions()

@app.cli.command('seed-admin')
@with_appcontext
def seed_admin():
    seed_admin_user()

@app.cli.command('seed-all')
@with_appcontext
def seed_all():
    run_seeders()


if __name__ == '__main__':
    port= os.getenv('PORT',4500)
    debug=os.getenv('FLASK_DEBUG',"False")=="True"
    app.run(port=port,debug=debug)