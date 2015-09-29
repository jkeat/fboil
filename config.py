import os


class BaseConfig(object):
	# general
	BASE_DIR = os.path.abspath(os.path.dirname(__file__))
	SECRET_KEY = os.environ.get('SECRET_KEY')

	# flask-security
	SECURITY_REGISTERABLE = True
	SECURITY_RECOVERABLE = True
	SECURITY_CONFIRMABLE = True
	SECURITY_CHANGEABLE = True
	SECURITY_USER_IDENTITY_ATTRIBUTES = 'email,username'
	SECURITY_LOGIN_WITHOUT_CONFIRMATION = True
	# Logged-in users are asked via users/confirm-email.html if they want a confirmation
	# link re-sent when they try to access a page that requires confirmation, so
	# this isn't needed and the 404 page is given instead. Is there a better way to do this?
	SECURITY_SEND_CONFIRMATION_TEMPLATE = "errors/404.html"  # prompt
	SECURITY_PASSWORD_HASH = "bcrypt"
	SECURITY_PASSWORD_SALT = os.environ.get('SECURITY_PASSWORD_SALT')

	# mail settings
	MAIL_SERVER = 'smtp.googlemail.com'
	MAIL_PORT = 465
	MAIL_USE_TLS = False
	MAIL_USE_SSL = True

	# mail account
	MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
	MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
	MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER')

	# misc
	SECONDS_TO_CHANGE_USERNAME = 900  # == 15 minutes for oauth user to change username


class DevelopmentConfig(BaseConfig):
	DEBUG = True
	SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/fboil'
	HOST = 'localhost'
	PORT = int(os.environ.get('PORT', 5000))


class TestingConfig(DevelopmentConfig):
	TESTING = True
	SQLALCHEMY_DATABASE_URI = "postgresql://localhost/fboil_test"
	WTF_CSRF_ENABLED = False


class ProductionConfig(BaseConfig):
	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

