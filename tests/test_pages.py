from flask import url_for
from .helpers import BaseTestCase, BaseUserTestCase
from flask.ext.security.core import current_user


class PageViewsTests(BaseTestCase):
    def test_about_page_load(self):
        response = self.client.get(url_for('pages.about'))
        self.assert200(response, message="About page didn't load")

    def test_home_page_load(self):
        response = self.client.get(url_for('pages.home'))
        self.assert200(response, message="Home page didn't load")

    def test_secret_page_anonymous_user_unconfirmed_email(self):
        """
        login_required is disabled on TESTING = True so it doesn't redirect to
        /login like it would for a logged out user
        """
        response = self.client.get(url_for('pages.secret'))
        self.assertRedirects(response, url_for('users.need_confirm_email'))


class PageViewsLoggedInTests(BaseUserTestCase):
    def test_secret_page_logged_in_unconfirmed_email(self):
        with self.client:
            self.login_user()
            response = self.client.get(url_for('pages.secret'))
            self.assertRedirects(response, url_for('users.need_confirm_email'))


class PageViewsConfirmedEmailTests(BaseUserTestCase):
    def test_secret_page_confirmed_email(self):
        self.confirm_user()
        self.login_user()
        if current_user.is_anonymous():
            print("In secret page test, user IS anonymous")
        else:
            print("In secret page test, user is NOT anonymous")
        response = self.client.get(url_for('pages.secret'))
        self.assert200(response)
