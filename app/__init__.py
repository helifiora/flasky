from flask import Flask, render_template
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from config import Config, ConfigEnum, create_config

mail = Mail()
db = SQLAlchemy()


def create_app(config_name: str):

    config = create_config(ConfigEnum.parse(config_name))

    app = Flask(__name__)
    app.config.from_object(config)

    from .main import main as mainbp
    from .auth import auth as authbp
    app.register_blueprint(mainbp)
    app.register_blueprint(authbp)

    config.init_app(app)
    mail.init_app(app)
    db.init_app(app)

    return app
