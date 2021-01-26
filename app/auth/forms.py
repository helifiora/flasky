from wtforms import Form, StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, Length


class LoginForm(Form):

    email = StringField(validators=[Email(), DataRequired(), Length(1, 64)])
    password = PasswordField(validators=[DataRequired()])
    remember_me = BooleanField()
