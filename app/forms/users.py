from flask.ext.login import current_user
from flask_wtf import Form
from wtforms import TextField, ValidationError
from wtforms.validators import DataRequired, Length
from ..models.users import User
from ..extensions import db

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
