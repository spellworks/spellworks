# -*- coding:utf-8 -*-
__author__ = 'zeno guo'

from flask import Flask
from flask.ext.wtf import CsrfProtect
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.mail import Mail


csrf = CsrfProtect()
db = SQLAlchemy()
mail = Mail()


def create_app(config_name):
    app = Flask(__name__)

    from config import config
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)
    csrf.init_app(app)
    mail.init_app(app)

    return app
