from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'

def create_app(database='sqlite:///site.db'):
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'Programowanie_w_języku_Python'
    app.config['SQLALCHEMY_DATABASE_URI'] = database
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    from app.blueprints.main import main
    from app.blueprints.auth import auth
    from app.blueprints.posts import posts
    from app.blueprints.errors import errors

    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(posts)
    app.register_blueprint(errors)

    with app.app_context():
        db.create_all()

    return app