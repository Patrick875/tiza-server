from flask import Flask
from config import Config 
from auth.routes import auth_bp
from users.routes import users_bp
from listings.routes import listings_bp
from categories.routes import categories_bp

url_prefix='/api/v1'

def create_app():
    app=Flask(__name__)
    app.config.from_object(Config)

    from extensions import db, migrate,jwt,mail

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    mail.init_app(app)
    
    import db.models

    app.register_blueprint(auth_bp,url_prefix=url_prefix+'/auth')
    app.register_blueprint(users_bp,url_prefix=url_prefix+'/users')
    app.register_blueprint(listings_bp,url_prefix=url_prefix+"/listings")
    app.register_blueprint(categories_bp,url_prefix=url_prefix+'/categories')


    return app

