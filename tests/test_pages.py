from flask import url_for
from .helpers import BaseTestCase


class PageViewsTests(BaseTestCase):
    def test_about_page_load(self):
        response = self.client.get(url_for('pages.about'))
        self.assert200(response, message="About page didn't load")

    def test_home_page_load(self):
        response = self.client.get(url_for('pages.home'))
        self.assert200(response, message="Home page didn't load")
