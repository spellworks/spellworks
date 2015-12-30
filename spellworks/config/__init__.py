# -*- coding:utf-8 -*-
__author__ = 'zeno guo'

import os
from errors import configure_errorhandlers
from blueprints import regist_blueprint


class Config:

    #: 表单通用秘钥
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'the answer of life, universe and everything'
    #: 管理员账号密码，设置在系统环境变量中
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')

    MAIL_SERVER = 'smtp.mxhichina.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    FLASKY_MAIL_SUBJECT_PREFIX = u"[SpellWorks]"

    WEBPACK_MANIFEST_PATH = './static/build/manifest.json'

    @staticmethod
    def init_app(app):  #: 初始化
        app.jinja_env.add_extension('pyjade.ext.jinja.PyJadeExtension')
        configure_errorhandlers(app)
        regist_blueprint(app)


class DevelopmentConfig(Config):
    DEBUG = True
    MONGODB_SETTINGS = {
        'db': 'spellworks',
        'host': os.environ.get('DEV_DATABASE_URL') or
        'mongodb://admin:0.618033@localhost:27111/spellworks',
    }


class TestingConfig(Config):
    TESTING = True
    MONGODB_SETTINGS = {
        'db': 'spellworks',
        'host': os.environ.get('DEV_DATABASE_URL') or
        'mongodb://admin:0.618033@localhost:27111/spellworks',
    }


config = {
    'default': DevelopmentConfig,
    'testing': TestingConfig,
}
