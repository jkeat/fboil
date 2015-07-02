from flask import url_for
from flask.ext.login import current_user
from app import User
from .helpers import BaseTestCase, BaseUserTestCase


class UserViewsTests(BaseTestCase):
    def test_register_page_load(self):
        response = self.client.get(url_for('users.register'))
        self.assert200(response, message="Signup page didn't load")

    def test_login_page_load(self):
        response = self.client.get(url_for('users.login'))
        self.assert200(response, message="Log in page didn't load")


class UserRegisterTests(BaseUserTestCase):
    def test_can_user_register(self):
        with self.client:
            user_data = {"username": self.USER2_USERNAME,
                         "email": self.USER2_EMAIL,
                         "password": self.USER2_PASSWORD,
                         "confirm": self.USER2_PASSWORD}
            response = self.client.post(url_for("users.register"),
                                        data=user_data)
            self.assert_redirects(response, url_for("pages.home"))

    def test_prevent_user_registering_with_taken_username(self):
        with self.client:
            user_data = {"username": self.USER_USERNAME,
                         "email": self.USER2_EMAIL,
                         "password": self.USER2_PASSWORD,
                         "confirm": self.USER2_PASSWORD}
            response = self.client.post(url_for("users.register"),
                                        data=user_data)
            self.assert200(response)
            self.assertIsNone(User.query.filter_by(email=self.USER2_EMAIL).first())


class UserLoginTests(BaseUserTestCase):
    def test_can_user_login_with_username(self):
        with self.client:
            response = self.client.post(url_for('users.login'),
                                        data={"username": self.USER_USERNAME,
                                              "password": self.USER_PASSWORD})
            self.assert_redirects(response, url_for("pages.home"))
            self.assertEqual(current_user.username, self.USER_USERNAME)

    def test_can_user_login_with_email(self):
        with self.client:
            response = self.client.post(url_for('users.login'),
                                        data={"username": self.USER_EMAIL,
                                              "password": self.USER_PASSWORD})
            self.assert_redirects(response, url_for("pages.home"))
            self.assertEqual(current_user.username, self.USER_USERNAME)


class UserLogoutTests(BaseUserTestCase):
    def test_can_user_logout(self):
        with self.client:
            self.login_user()
            self.assertIsNotNone(current_user.get_id())
            self.logout_user()
            self.assertIsNone(current_user.get_id())
