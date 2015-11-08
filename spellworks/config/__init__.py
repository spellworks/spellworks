# -*- coding:utf-8 -*-
__author__ = 'zeno guo'

import os
from errors import configure_errorhandlers
from blueprints import regist_blueprint


class Config:

    #: 表单通用秘钥
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'the answer of life, universe and everything'
    #: sqlalchemy配置项，设置为true后每次请求结束后自动提交数据库中的变动
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    #: 管理员账号密码，设置在系统环境变量中
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')

    @staticmethod
    def init_app(app):  #: 初始化
        configure_errorhandlers(app)
        regist_blueprint(app)


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'mysql://root:0.618033@localhost/spellworks'


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'mysql://root:0.618033@localhost/spellworks'


config = {
    'default': DevelopmentConfig,
    'testing': TestingConfig,
}
