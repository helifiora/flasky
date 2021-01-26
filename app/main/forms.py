from wtforms import Form, StringField
from wtforms.validators import DataRequired


class NameForm(Form):
    name = StringField('Name', [DataRequired('Name is required!')])
