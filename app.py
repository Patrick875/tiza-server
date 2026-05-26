from flask import Flask
from config import Config 
from auth.routes import auth_bp
from users.routes import users_bp

url_prefix='/api/v1'

def create_app():
    app=Flask(__name__)
    app.config.from_object(Config)

    from extensions import db, migrate,jwt,mail

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    mail.init_app(app)
    
    import users.models
    import profiles.models
    import auth.models
    import orders.models
    import cart.models
    import listings.models
    import rentals.models

    app.register_blueprint(auth_bp,url_prefix=url_prefix+'/auth')
    app.register_blueprint(users_bp,url_prefix=url_prefix+'/users')


    return app

