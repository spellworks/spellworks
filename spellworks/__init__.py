# -*- coding:utf-8 -*-
__author__ = 'zeno guo'

from flask import Flask
from flask.ext.wtf import CsrfProtect
from flask.ext.mail import Mail
from flask.ext.mongoengine import MongoEngine


csrf = CsrfProtect()
db = MongoEngine()
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
