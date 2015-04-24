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
        if not Form.validate(self):
            return False

        user = User.query.filter(or_(  # TODO: works? add post control
            User.username == self.username.data.lower(),
            User.email == self.email.data.lower())).first()
        if user:
            self.email.errors.append("That email is already taken")
            return False
        else:
            return True


class LoginForm(Form):
    name = TextField('Username', [DataRequired()])
    password = PasswordField('Password', [DataRequired()])


class ForgotForm(Form):
    email = TextField(
        'Email', validators=[DataRequired(), Length(min=6, max=40)]
    )
