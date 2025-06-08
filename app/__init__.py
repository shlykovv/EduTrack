from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager


db = SQLAlchemy()
migrate = Migrate()
login_manger = LoginManager()
login_manger.login_view = 'auth.login'


def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    
    db.init_app(app)
    migrate.init_app(app, db)
    login_manger.init_app(app)
    
    from app.routes import main
    from app.auth import auth_bp
    from app.courses import course_bp
    from app.profile import profile_bp
    
    app.register_blueprint(main)
    app.register_blueprint(auth_bp)
    app.register_blueprint(course_bp)
    app.register_blueprint(profile_bp)
    
    return app
