from ctypes import Union
from flask import Flask, render_template, request
from wtforms import Form, StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)


class NameForm(Form):
    name = StringField('Name', [DataRequired('Name is required!')])


@app.route('/', methods=['GET', 'POST'])
def index():
    name = None

    if request.method == 'POST':
        form = NameForm(request.form)
        if form.validate():
            name = request.form['name']

    return render_template('index.html', name=name)


@app.route('/user/<string:name>')
def user(name: str):
    return render_template('user.html', name=name)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html')
