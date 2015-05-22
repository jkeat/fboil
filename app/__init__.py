from flask import Flask
from .extensions import login_manager, db, mail, serializer

from .models import *

from .controllers.pages import pages
from .controllers.users import users

BLUEPRINTS = (
    pages,
    users,
)


def create_app(config_filename):
    app = Flask(__name__)
    app.config.from_object(config_filename)

    configure_blueprints(app, BLUEPRINTS)
    configure_extensions(app)

    return app


def configure_extensions(app):
    # flask-login
    login_manager.login_view = 'users.login'
    login_manager.login_message = 'Log in required.'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)
    login_manager.init_app(app)

    # flask-sqlalchemy
    db.init_app(app)

    # flask-mail
    mail.init_app(app)

    # serialize
    serializer.init_app(app)


def configure_blueprints(app, blueprints):
    for blueprint in blueprints:
        app.register_blueprint(blueprint)
