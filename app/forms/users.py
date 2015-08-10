from flask.ext.login import current_user
from flask_wtf import Form
from wtforms import TextField, PasswordField, ValidationError
from wtforms.validators import DataRequired, EqualTo, Length, Email
from ..models.users import User
from ..extensions import db


class RegisterForm(Form):
    username = TextField(
        'Username', validators=[DataRequired(), Length(
            min=3, max=25,
            message="Username must be between 3 and 25 characters.")]
    )
    email = TextField(
        'Email', validators=[DataRequired(), Email()]
    )
    password = PasswordField(
        'Password', validators=[DataRequired(), Length(
            min=6,
            message="Password must be at least 6 characters.")]
    )
    confirm = PasswordField(
        'Confirm Password',
        [DataRequired(),
            EqualTo('password', message='Passwords must match')]
    )

    def validate_username(self, field):
        if User.is_username_taken(field.data):
            raise ValidationError("That username is already taken")

    def validate_email(self, field):
        if User.is_email_taken(field.data):
            raise ValidationError("That email is already in use")

    def create_user(self):
        new_user = User(username=self.username.data,
                        email=self.email.data,
                        password=self.password.data)
        db.session.add(new_user)
        db.session.commit()
        return new_user


class LoginForm(Form):
    username = TextField('Username or Email', [DataRequired()])
    password = PasswordField('Password', [DataRequired()])

    def validate(self):
        if not Form.validate(self):
            return False

        user = self.get_user()
        if not user:
            self.username.errors.append("Hah, wrong. Try again.")
            return False
        return True

    def get_user(self):
        user = User.get_by_email_or_username(self.username.data)
        if user and user.passhash:
            if user.check_password(self.password.data):
                return user


class ForgotPasswordForm(Form):
    email = TextField(
        'Email', validators=[DataRequired(), Email()]
    )

    def validate_email(self, field):
        if not User.is_email_taken(field.data):
            raise ValidationError("Email not found. Try again!")


class ResetPasswordForm(Form):
    password = PasswordField(
        'New password', validators=[DataRequired(), Length(
            min=6,
            message="Password must be at least 6 characters.")]
    )
    confirm = PasswordField(
        'Confirm new password',
        [DataRequired(),
            EqualTo('password', message='Passwords must match')]
    )

    def change_password(self, user):
        user.set_password(self.password.data)
        db.session.add(user)
        db.session.commit()


class SetUsernameForm(Form):
    username = TextField(
        'New username', validators=[DataRequired(), Length(
            min=3, max=25,
            message="Username must be between 3 and 25 characters.")]
    )

    def validate_username(self, field):
        if field.data.lower() != current_user.username.lower() and User.is_username_taken(field.data):
            raise ValidationError("That username is already taken")

    def set_username(self, user_id):
        if not current_user.username == self.username.data:
            user = User.query.get(user_id)
            user.username = self.username.data
            db.session.add(user)
            db.session.commit()
