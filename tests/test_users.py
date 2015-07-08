from flask import url_for
from flask.ext.login import current_user
from app import User
from .helpers import BaseTestCase, BaseUserTestCase
from app.extensions import serializer


class UserModelTests(BaseUserTestCase):
    def test_user_to_string(self):
        self.assertEqual(str(self.user), "<User {0}>".format(self.USER_USERNAME))

    def test_confirm_email(self):
        self.assertFalse(self.user.confirmed_email)
        self.user.confirm_email()
        self.assertTrue(self.user.confirmed_email)


class UserViewsTests(BaseTestCase):
    def test_register_page_load(self):
        response = self.client.get(url_for('users.register'))
        self.assert200(response, message="Signup page didn't load")

    def test_login_page_load(self):
        response = self.client.get(url_for('users.login'))
        self.assert200(response, message="Log in page didn't load")


class UserRegisterTests(BaseUserTestCase):
    def test_can_user_register(self):
        user_data = {"username": self.USER2_USERNAME,
                     "email": self.USER2_EMAIL,
                     "password": self.USER2_PASSWORD,
                     "confirm": self.USER2_PASSWORD}
        response = self.client.post(url_for("users.register"),
                                    data=user_data)
        self.assert_redirects(response, url_for("pages.home"))

    def test_prevent_user_registering_with_taken_username(self):
        user_data = {"username": self.USER_USERNAME,
                     "email": self.USER2_EMAIL,
                     "password": self.USER2_PASSWORD,
                     "confirm": self.USER2_PASSWORD}
        response = self.client.post(url_for("users.register"),
                                    data=user_data)
        self.assert200(response)
        self.assertIsNone(User.query.filter_by(email=self.USER2_EMAIL).first())

    def test_prevent_user_registering_with_taken_email(self):
        user_data = {"username": self.USER2_USERNAME,
                     "email": self.USER_EMAIL,
                     "password": self.USER2_PASSWORD,
                     "confirm": self.USER2_PASSWORD}
        response = self.client.post(url_for("users.register"),
                                    data=user_data)
        self.assert200(response)
        self.assertIsNone(User.query.filter_by(email=self.USER2_USERNAME).first())


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

    def test_prevent_user_login_with_wrong_password(self):
        response = self.client.post(url_for('users.login'),
                                    data={"username": self.USER_EMAIL,
                                          "password": self.USER_PASSWORD + "789"})
        self.assertTemplateUsed('users/forms/login.html')

    def test_prevent_login_no_username_sent(self):
        response = self.client.post(url_for('users.login'),
                                    data={"username": "",
                                          "password": self.USER_PASSWORD})
        self.assertTemplateUsed('users/forms/login.html')


class UserLogoutTests(BaseUserTestCase):
    def test_can_user_logout(self):
        with self.client:
            self.login_user()
            self.assertIsNotNone(current_user.get_id())
            self.logout_user()
            self.assertIsNone(current_user.get_id())


class ConfirmEmailViewTests(BaseUserTestCase):
    def test_prevent_anonymous_user_viewing_confirm_email_page(self):
        response = self.client.get(url_for('users.need_confirm_email'))
        self.assert_redirects(response, url_for('users.login'))

    def test_can_logged_in_user_view_confirmed_email_page(self):
        self.login_user()
        response = self.client.get(url_for('users.need_confirm_email'))
        self.assert200(response)


class ForgotPasswordViewTests(BaseUserTestCase):
    def test_forgot_password_page_load(self):
        response = self.client.get(url_for('users.forgot_password'))
        self.assert200(response)

    def test_can_user_submit_email_for_password_reset(self):
        response = self.client.post(url_for('users.forgot_password'),
                                    data={"email": self.USER_EMAIL})
        self.assert_redirects(response, url_for('users.login'))

    def test_prevent_user_submit_incorrect_email_for_password_reset(self):
        response = self.client.post(url_for('users.forgot_password'),
                                    data={"email": "catalina@descend.nets"})
        self.assert200(response)

    def test_prevent_logged_in_user_viewing(self):
        self.login_user()
        response = self.client.get(url_for('users.forgot_password'))
        self.assert_redirects(response, url_for('pages.home'))


class ConfirmUserViewTests(BaseUserTestCase):
    def test_can_confirm_user_email(self):
        self.assertFalse(self.user.confirmed_email)
        user_id_token = serializer.serialize_data(self.user.id)
        confirm_url = url_for('users.confirm_user', token=user_id_token)
        response = self.client.get(confirm_url)
        self.assert_redirects(response, url_for('pages.home'))
        self.assertTrue(self.user.confirmed_email)

    def test_user_id_from_token_does_not_exist_404(self):
        user_does_not_exist_id_token = serializer.serialize_data(self.user.id + 50)
        confirm_url = url_for('users.confirm_user', token=user_does_not_exist_id_token)
        response = self.client.get(confirm_url)
        self.assert404(response)
        self.assertFalse(self.user.confirmed_email)

    def test_user_id_token_bad_signature_404(self):
        bad_user_id_token = list(serializer.serialize_data(self.user.id))
        bad_user_id_token[1:7] = "RaNdOm"
        confirm_url = url_for('users.confirm_user', token=bad_user_id_token)
        response = self.client.get(confirm_url)
        self.assert404(response)
        self.assertFalse(self.user.confirmed_email)

    def test_user_email_already_confirmed(self):
        self.user.confirm_email()
        self.assertTrue(self.user.confirmed_email)
        user_id_token = serializer.serialize_data(self.user.id)
        confirm_url = url_for('users.confirm_user', token=user_id_token)
        response = self.client.get(confirm_url)
        self.assert_redirects(response, url_for('pages.home'))
        self.assertTrue(self.user.confirmed_email)


class ResendConfirmationEmailViewTests(BaseUserTestCase):
    def test_resend_confirmation_email(self):
        self.login_user()
        response = self.client.get(url_for('users.resend_confirmation_email'))
        self.assert_redirects(response, url_for('pages.home'))

    def test_prevent_resend_confirmation_email_already_confirmed_email(self):
        self.user.confirm_email()
        self.login_user()
        response = self.client.get(url_for('users.resend_confirmation_email'))
        self.assert_redirects(response, url_for('pages.home'))


class ResetPasswordViewTests(BaseUserTestCase):
    def test_reset_password_page_load(self):
        user_email_token = serializer.serialize_timed_data(self.user.email)
        reset_password_url = url_for('users.reset_password', token=user_email_token)
        response = self.client.get(reset_password_url)
        self.assert200(response)

    def test_prevent_reset_password_page_load_bad_token(self):
        bad_user_email_token = list(serializer.serialize_timed_data(self.user.email))
        bad_user_email_token[1:7] = "rAnDoM"
        reset_password_url = url_for('users.reset_password', token=bad_user_email_token)
        response = self.client.get(reset_password_url)
        self.assert404(response)

    def test_prevent_reset_password_page_load_email_not_exist(self):
        user_does_not_exist_email_token = serializer.serialize_timed_data("catalina@descend.nets")
        reset_password_url = url_for('users.reset_password', token=user_does_not_exist_email_token)
        response = self.client.get(reset_password_url)
        self.assert404(response)

    def test_reset_password(self):
        NEW_PASSWORD = "NEW-PASSWORD-33"
        self.assertTrue(self.user.check_password(self.USER_PASSWORD))
        user_email_token = serializer.serialize_timed_data(self.user.email)
        reset_password_url = url_for('users.reset_password', token=user_email_token)
        response = self.client.post(reset_password_url,
                                    data={"password": NEW_PASSWORD,
                                          "confirm": NEW_PASSWORD})
        self.assertFalse(self.user.check_password(self.USER_PASSWORD))
        self.assertTrue(self.user.check_password(NEW_PASSWORD))

    def test_prevent_reset_password_if_confirm_does_not_match(self):
        NEW_PASSWORD = "NEW-PASSWORD-33"
        self.assertTrue(self.user.check_password(self.USER_PASSWORD))
        user_email_token = serializer.serialize_timed_data(self.user.email)
        reset_password_url = url_for('users.reset_password', token=user_email_token)
        response = self.client.post(reset_password_url,
                                    data={"password": NEW_PASSWORD,
                                          "confirm": "NOT-THE-SAME"})
        self.assertTrue(self.user.check_password(self.USER_PASSWORD))
        self.assertFalse(self.user.check_password(NEW_PASSWORD))

    def test_prevent_reset_password_if_bad_token(self):
        NEW_PASSWORD = "NEW-PASSWORD-33"
        self.assertTrue(self.user.check_password(self.USER_PASSWORD))
        bad_user_email_token = list(serializer.serialize_timed_data(self.user.email))
        bad_user_email_token[1:7] = "rAnDoM"
        reset_password_url = url_for('users.reset_password', token=bad_user_email_token)
        response = self.client.post(reset_password_url,
                                    data={"password": NEW_PASSWORD,
                                          "confirm": NEW_PASSWORD})
        self.assertTrue(self.user.check_password(self.USER_PASSWORD))
        self.assertFalse(self.user.check_password(NEW_PASSWORD))
        self.assert404(response)

    def test_prevent_reset_password_if_bad_token(self):
        NEW_PASSWORD = "NEW-PASSWORD-33"
        self.assertTrue(self.user.check_password(self.USER_PASSWORD))
        user_does_not_exist_email_token = serializer.serialize_timed_data("catalina@descend.nets")
        reset_password_url = url_for('users.reset_password', token=user_does_not_exist_email_token)
        response = self.client.post(reset_password_url,
                                    data={"password": NEW_PASSWORD,
                                          "confirm": NEW_PASSWORD})
        self.assertTrue(self.user.check_password(self.USER_PASSWORD))
        self.assertFalse(self.user.check_password(NEW_PASSWORD))
        self.assert404(response)
