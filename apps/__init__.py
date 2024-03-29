# -*- encoding: utf-8 -*-
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from importlib import import_module
from flask_wtf.csrf import CSRFProtect, CSRFError

from flask import Flask

app = Flask(__name__)
db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect(app)

def register_extensions(app):
    db.init_app(app)
    login_manager.init_app(app)


def register_blueprints(app):
    for module_name in ('authentication', 'home'):
        module = import_module('apps.{}.routes'.format(module_name))
        app.register_blueprint(module.blueprint)


def configure_database(app):

    @app.before_first_request
    def initialize_database():
        db.create_all()

    @app.teardown_request
    def shutdown_session(exception=None):
        db.session.remove()

def create_app(config):
    app.config.from_object(config)
    register_extensions(app)
    csrf.init_app(app)

    register_blueprints(app)
    configure_database(app)
    return app
