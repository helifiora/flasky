from enum import Enum
import os
from abc import ABC
from typing import Type
from flask import Flask

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(ABC):

    # Key
    SECRET_KEY = os.environ.get('SECRET_KEY', 'hard to guess string')

    # Mail
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.googlemail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', '587'))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in [
        'true', 'on', 1]
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

    FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
    FLASKY_MAIL_SENDER = 'Flasky Admin <flasky@example.com>'
    FLASK_ADMIN = os.environ.get('FLASKY_ADMIN')

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app: Flask):
        ...


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DEV_DATABASE_URL', 'postgresql://postgres:postgres@localhost/flasky')


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'TEST_DATABASE_URL', 'sqlite:///test.db')


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'PROD_DATABASE_URL', 'sqlite:///prod.db')


class ConfigEnum(Enum):
    DEVELOPMENT = 'development'
    TESTING = 'testing'
    PRODUCTION = 'production'

    @staticmethod
    def parse(value: str) -> 'ConfigEnum':
        has_value = value in [x.value for x in ConfigEnum.__members__.values()]
        if has_value:
            return ConfigEnum(value)
        else:
            return ConfigEnum.DEVELOPMENT


def create_config(config: ConfigEnum) -> Type[Config]:
    if config == ConfigEnum.DEVELOPMENT:
        return DevelopmentConfig

    if config == ConfigEnum.TESTING:
        return TestingConfig

    if config == ConfigEnum.PRODUCTION:
        return ProductionConfig

    return DevelopmentConfig
