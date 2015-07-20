import os

DEBUG = True
SECRET_KEY = os.environ['SECRET_KEY']
SECURITY_PASSWORD_SALT = os.environ['SECURITY_PASSWORD_SALT']
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/fboil'
HOST = 'localhost'
PORT = int(os.environ.get('PORT', 5000))

# mail settings
MAIL_SERVER = 'smtp.googlemail.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True

# mail account
MAIL_USERNAME = os.environ['MAIL_USERNAME']
MAIL_PASSWORD = os.environ['MAIL_PASSWORD']
MAIL_DEFAULT_SENDER = os.environ['MAIL_DEFAULT_SENDER']

# misc
SECONDS_TO_CHANGE_USERNAME = 900  # == 15 minutes for oauth user to change username

