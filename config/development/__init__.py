import os

DEBUG = True
SECRET_KEY = 'myprecious'
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/flask_boilerplate'
HOST = 'localhost'
PORT = int(os.environ.get('PORT', 5000))

# mail settings
MAIL_SERVER = 'smtp.googlemail.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True

# gmail authentication
MAIL_USERNAME = "company-email"  # TODO make environ variable
MAIL_PASSWORD = "coding69"  # TODO ^^

# mail accounts
MAIL_DEFAULT_SENDER = 'company-email@example.com'
