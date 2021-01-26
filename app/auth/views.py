from flask_login import login_required, login_user, logout_user
from app.models import User
from app.auth.forms import LoginForm, RegistrationForm
from flask import flash, render_template, request, url_for, redirect
from . import auth
from .. import db


@auth.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        form = LoginForm(request.form)
        if form.validate():
            user: User = User.query.filter_by(
                email=request.form['email']).first()
            if user is not None and user.verify_password(request.form['password']):
                login_user(user, request.form.get('logged', False))
                next = request.args.get('next', None)
                if next is None or not next.startswith('/'):
                    next = url_for('main.index')
                return redirect(next)
            flash('Invalid username or password')

    return render_template('auth/login.html')


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))


@auth.route('/register', methods=['POST', 'GET'])
def register():

    form = RegistrationForm()
    if request.method == 'POST':
        form = RegistrationForm(request.form)
        if form.validate():
            user = User(email=form.email.data,
                        username=form.username.data, password=form.password.data)
            db.session.add(user)
            db.session.commit()
            flash('You can now login.')
            return redirect(url_for('auth.login'))

    return render_template('auth/register.html')
