# -*- coding:utf-8 -*-
__author__ = 'zeno guo'

from main import main as main_blueprint
from auth import auth as auth_blueprint
from spellworks.user import user as user_blueprint


def regist_blueprint(app):
    app.register_blueprint(main_blueprint)
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(user_blueprint)
