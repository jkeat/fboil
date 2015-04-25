from flask_wtf import Form
from sqlalchemy import or_
from wtforms import TextField, PasswordField
from wtforms.validators import DataRequired, EqualTo, Length
from models import *


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
        'Repeat Password',
        [DataRequired(),
            EqualTo('password', message='Passwords must match')]
    )

    def validate(self):
        return_boolean = True  # to allow all errors to be appended

        if not Form.validate(self):
            return_boolean = False

        user_username = User.query.filter_by(
            username=self.username.data.lower()).first()
        if user_username:
            self.email.errors.append("That username is already taken")
            return_boolean = False

        user_email = User.query.filter_by(
            email=self.email.data.lower()).first()
        if user_email:
            self.email.errors.append("That email is already taken")
            return_boolean = False

        return return_boolean

    def create_user(self):
        new_user = User(username=self.username.data.lower(),
                        email=self.email.data.lower(),
                        password=self.password.data.lower())
        db.session.add(new_user)
        db.session.commit()
        return new_user


class LoginForm(Form):
    name = TextField('Username', [DataRequired()])
    password = PasswordField('Password', [DataRequired()])


class ForgotForm(Form):
    email = TextField(
        'Email', validators=[DataRequired(), Length(min=6, max=40)]
    )
