from flask import Flask, render_template

app = Flask(__name__)


def index():
    return render_template('index.html')


def user(name: str):
    return render_template('user.html', name=name)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html')


app.add_url_rule('/', 'index', index)
app.add_url_rule('/user/<string:name>', 'user', user)
