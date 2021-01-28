from app.email import send_email
from flask_login import current_user, login_required, login_user, logout_user
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
            token = user.generate_confirmation_token()
            send_email(user.email, 'Confirm Your Account',
                       'auth/mail/confirm', user=user, token=token)
            flash('You can now login.')
            return redirect(url_for('auth.login'))

    return render_template('auth/register.html')


@auth.route('/confirm/<string:token>')
@login_required
def confirm(token: str):
    if current_user.confirmed:
        return redirect(url_for('main.index'))

    if current_user.confirm(token):
        db.session.commit()
        flash('You have confirmed your account. Thanks!')
    else:
        flash('The confirmation link is invalid or has expired!')

    return redirect(url_for('main.index'))


@auth.before_app_request
def before_request():
    if current_user.is_authenticated \
            and not current_user.confirmed \
            and request.blueprint != 'auth' \
            and request.endpoint != 'static':
        return redirect(url_for('auth.unconfirmed'))


@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))

    return render_template('auth/unconfirmed.html')


@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, 'Confirm Your Account',
               'auth/email/confirm', user=current_user, token=token)
    flash('A new confirmation email has been sent to you by email')
    return redirect(url_for('main.index'))
