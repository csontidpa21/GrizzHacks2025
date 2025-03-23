from flask import Flask
from config import Config
from .extensions import db, migrate, login_manager, bcrypt

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize Extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    
    # Blueprints
    from .auth import auth
    from .routes import main
    from .shop import shop
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(main)
    app.register_blueprint(shop, url_prefix='/shop')

    return app
