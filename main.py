from flask import Flask

app = Flask(__name__)


def index():
    return '<h1>Hello World!</h1>'


def user(name: str):
    return f'<h2>Hello {name}</h2>'


app.add_url_rule('/', 'index', index)
app.add_url_rule('/user/<string:name>', 'user', user)
