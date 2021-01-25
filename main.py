from flask import Flask, render_template, request, session, url_for, redirect, flash
from wtforms import Form, StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'my super key'


class NameForm(Form):
    name = StringField('Name', [DataRequired('Name is required!')])


@app.route('/', methods=['GET', 'POST'])
def index():

    if request.method == 'POST':
        form = NameForm(request.form)
        if form.validate():
            name = request.form['name']
            old_name = session.get('name')

            session['name'] = name

            if old_name is not None and old_name != name:
                flash('Looks like you have changed your name!')

        return redirect(url_for('index'))

    return render_template('index.html', name=session.get('name'))


@app.route('/user/<string:name>')
def user(name: str):
    return render_template('user.html', name=name)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html')
