from flask import Flask, render_template, request, session, url_for, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from wtforms import Form, StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'my super key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/flasky'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self) -> str:
        return f'<Role {self.name}>'


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self) -> str:
        return f'<User {self.username}>'


class NameForm(Form):
    name = StringField('Name', [DataRequired('Name is required!')])


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        form = NameForm(request.form)
        if form.validate():

            name = request.form['name']
            user = User.query.filter_by(username=name).first()
            if user is None:
                user = User(username=name)
                db.session.add(user)
                db.session.commit()
                session['known'] = False
            else:
                session['known'] = True

            old_name = session.get('name')

            session['name'] = name

            if old_name is not None and old_name != name:
                flash('Looks like you have changed your name!')

        return redirect(url_for('index'))

    return render_template('index.html', name=session.get('name'), known=session.get('known'))


@app.route('/user/<string:name>')
def user(name: str):
    return render_template('user.html', name=name)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html')
