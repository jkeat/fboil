from flask import url_for
from flask.ext.testing import TestCase
from flask.ext.login import current_user
from app import create_app, User
from app.extensions import db


class BaseTestCase(TestCase):
    def create_app(self):
        app = create_app('config.TestingConfig')
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()


class BaseUserTestCase(BaseTestCase):
    USER_USERNAME = "homer"
    USER_EMAIL = "hsimpson@donutmail.net"
    USER_PASSWORD = "mrPL0W_kl53226"

    USER2_USERNAME = "lisa"
    USER2_EMAIL = "lisa2000@rocketmail.com"
    USER2_PASSWORD = "n3lson_is_ha_hawt"

    def setUp(self):
        super(BaseUserTestCase, self).setUp()
        self.user = self.create_user(username=self.USER_USERNAME,
                                     email=self.USER_EMAIL,
                                     password=self.USER_PASSWORD)

    def create_user(self, **kwargs):
        user = User(**kwargs)
        db.session.add(user)
        db.session.commit()
        return user

    def create_second_user(self):
        self.user2 = self.create_user(username=self.USER2_USERNAME,
                                      email=self.USER2_EMAIL,
                                      password=self.USER2_PASSWORD)

    def login_user(self, username=None, password=None):
        if username is None:
            username = self.USER_USERNAME
        if password is None:
            password = self.USER_PASSWORD
        self.client.post(url_for('users.login'),
                         data={"username": username,
                               "password": password},
                         follow_redirects=True)

    def logout_user(self):
        self.client.get(url_for('users.logout'))
