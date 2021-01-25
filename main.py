from flask import Flask, render_template

app = Flask(__name__)


def index():
    return render_template('index.html')


def user(name: str):
    return render_template('user.html', name=name)


app.add_url_rule('/', 'index', index)
app.add_url_rule('/user/<string:name>', 'user', user)
