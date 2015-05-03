from flask.ext.login import LoginManager
login_manager = LoginManager()

from flask.ext.sqlalchemy import SQLAlchemy
db = SQLAlchemy()

from flask_mail import Mail
mail = Mail()
