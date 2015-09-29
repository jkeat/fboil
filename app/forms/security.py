from flask_security.forms import ConfirmRegisterForm
from wtforms import TextField, ValidationError
from wtforms.validators import InputRequired, Length
from ..models.users import User


class ExtendedConfirmRegisterForm(ConfirmRegisterForm):
	username = TextField(
        'Username', validators=[InputRequired(), Length(
            min=3, max=25,
            message="Username must be between 3 and 25 characters.")]
    )

	def validate_username(self, field):
		if User.is_username_taken(field.data):
			raise ValidationError("That username is already taken.")
