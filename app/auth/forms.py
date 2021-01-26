from wtforms import Form, Field, StringField, PasswordField, BooleanField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Email, Length, Regexp, EqualTo
from ..models import User


class LoginForm(Form):

    email = StringField(validators=[Email(), DataRequired(), Length(1, 64)])
    password = PasswordField(validators=[DataRequired()])
    logged = BooleanField()


class RegistrationForm(Form):

    email = StringField('Email', validators=[
                        DataRequired(), Length(1, 64), Email()])
    username = StringField('Username', validators=[DataRequired(), Length(1, 64), Regexp(
        '^[A-Za-z][A-Za-z0-9_.]*$', 0, 'Usernames must have only letters, numbers, dots or underscores')])
    password = PasswordField('Password', validators=[
                             DataRequired(), EqualTo('password2', 'Passwords must match.')])
    password2 = PasswordField('Confirm Password', [DataRequired()])

    def validate_email(self, field: Field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    def validate_username(self, field: Field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')
