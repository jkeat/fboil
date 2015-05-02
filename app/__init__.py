from flask import Flask
from .extensions import login_manager, db

from app.controllers.pages import pages_blueprint
from app.models import User


BLUEPRINTS = (
    pages_blueprint,
)


def create_app():
    app = Flask(__name__)
    app.config.from_object('config.development')

    configure_blueprints(app, BLUEPRINTS)
    configure_extensions(app)

    return app


def configure_extensions(app):
    # flask-login
    login_manager.login_view = 'pages.login'
    login_manager.login_message = 'Log in required.'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)
    login_manager.init_app(app)

    # flask-sqlalchemy
    db.init_app(app)


def configure_blueprints(app, blueprints):
    for blueprint in blueprints:
        app.register_blueprint(blueprint)
