from flask_wtf import Form
from wtforms import TextField, PasswordField, ValidationError
from wtforms.validators import DataRequired, EqualTo, Length
from .models import User
from .extensions import db


class RegisterForm(Form):
    username = TextField(
        'Username', validators=[DataRequired(), Length(min=3, max=25)]
    )
    email = TextField(
        'Email', validators=[DataRequired(), Length(min=6, max=254)]
    )
    password = PasswordField(
        'Password', validators=[DataRequired(), Length(min=6, max=40)]
    )
    confirm = PasswordField(
        'Confirm Password',
        [DataRequired(),
            EqualTo('password', message='Must match')]
    )

    def validate_username(self, field):
        if User.query.filter_by(
                username=field.data.lower()).first() is not None:
            raise ValidationError("That username is already taken")

    def validate_email(self, field):
        if User.query.filter_by(email=field.data.lower()).first() is not None:
            raise ValidationError("That email is already taken")

    def create_user(self):
        new_user = User(username=self.username.data.lower(),
                        email=self.email.data.lower(),
                        password=self.password.data.lower())
        db.session.add(new_user)
        db.session.commit()
        return new_user


class LoginForm(Form):
    username = TextField('Username', [DataRequired()])
    password = PasswordField('Password', [DataRequired()])

    def validate(self):
        if not Form.validate(self):
            return False

        user = self.get_user()
        if not user:
            self.username.errors.append("Invalid login")
            return False
        return True

    def get_user(self):
        user = User.get_by_email_or_username(self.username.data.lower())
        if user:
            if user.check_password(self.password.data):
                return user


class ForgotForm(Form):
    email = TextField(
        'Email', validators=[DataRequired(), Length(min=6, max=254)]
    )
