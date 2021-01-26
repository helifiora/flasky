from flask import render_template, request, session, redirect, url_for
from datetime import datetime
from .forms import NameForm
from ..models import User
from .. import db
from . import main


@main.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        form = NameForm(request.form)
        if form.validate():
            return redirect(url_for('.index'))

    name = session.get('name')
    known = session.get('known', False)
    current_time = datetime.utcnow()
    return render_template('index.html', name=name, known=known, current_time=current_time)
