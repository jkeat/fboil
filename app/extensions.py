from flask.ext.login import LoginManager
login_manager = LoginManager()

from flask.ext.sqlalchemy import SQLAlchemy
db = SQLAlchemy()

from flask_mail import Mail
mail = Mail()

from .serialize import Serializer
serializer = Serializer()

import os
from flask_oauthlib.client import OAuth
oauth = OAuth()
twitter = oauth.remote_app('twitter',
    base_url='https://api.twitter.com/1.1/',
    request_token_url='https://api.twitter.com/oauth/request_token',
    access_token_url='https://api.twitter.com/oauth/access_token',
    authorize_url='https://api.twitter.com/oauth/authenticate',
    consumer_key=os.environ.get("TWITTER_CONSUMER_KEY"),  # use config value if in extensions?
    consumer_secret=os.environ.get("TWITTER_CONSUMER_SECRET")
)
from flask import session
@twitter.tokengetter
def get_twitter_token(token=None):
    return session.get('twitter_token')

from flask.ext.compress import Compress
compress = Compress()
