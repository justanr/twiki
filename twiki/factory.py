from .auth_keys import AuthKeys
from .config import configs, DefaultConfig

import os
from flask import Flask
from flask_bootstrap import Bootstrap


def create_app(config_name=None):
    "Setup a fully configured application and return it out for immediate use"
    app = Flask(__name__)

    config_app(app, config_name)
    init_exts(app)

    return app


def config_app(app, config_name=None):
    config = find_app_config(config_name)

    app.config.from_object(config)
    app.config.from_object(AuthKeys)

    if hasattr(config, 'init_app'):
        config.init_app(app)


def find_app_config(name=None):
    if name is None:
        name = get_config_from_env(default='default')

    return configs.get(name, DefaultConfig)


def get_config_from_env(default='default'):
    return os.environ.get('TWIKI_CONFIG', default)


def init_exts(app):
    Bootstrap(app)
