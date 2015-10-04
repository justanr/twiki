from .app import backend, frontend
from .auth_keys import AuthKeys
from .config import configs, DefaultConfig
from .exts import twitter
from .twitter import TwitterError
from .wiki import WikipediaError

import os
from flask import Flask, jsonify
from flask_bootstrap import Bootstrap


def create_app(config_name=None):
    "Setup a fully configured application and return it out for immediate use"
    app = Flask(__name__)

    config_app(app, config_name)
    init_exts(app)
    register_blueprints(app)
    register_handlers(app)

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
    twitter.init_app(app)


def register_handlers(app):
    @app.after_request
    def allow_cors(resp):
        resp.headers['Access-Control-Allow-Origin'] = '*'
        resp.headers['Access-Control-Allow-Methods'] = 'GET, OPTIONS, PUT'
        resp.headers['Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept'
        return resp

    @app.errorhandler(TwitterError)
    @app.errorhandler(WikipediaError)
    def handle_error(err):
        return jsonify(msg=err.msg), err.code


def register_blueprints(app):
    app.register_blueprint(frontend)
    app.register_blueprint(backend, url_prefix='/api')
