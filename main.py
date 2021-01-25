from flask import Flask, render_template, request, session, url_for, redirect
from wtforms import Form, StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'my super key'


class NameForm(Form):
    name = StringField('Name', [DataRequired('Name is required!')])


@app.route('/', methods=['GET'])
def get_index():
    return render_template('index.html', name=session.get('name'))


@app.route('/', methods=['POST'])
def post_index():
    form = NameForm(request.form)
    if form.validate():
        name = request.form['name']
        session['name'] = name

    return redirect(url_for('get_index'))


@app.route('/user/<string:name>')
def user(name: str):
    return render_template('user.html', name=name)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html')
