# -*- coding:utf-8 -*-
__author__ = 'zeno guo'

from main import main as main_blueprint
from login import login as login_blueprint
from spellworks.user import user as user_blueprint


def regist_blueprint(app):
    app.register_blueprint(main_blueprint)
    app.register_blueprint(login_blueprint, url_prefix='/login')
    app.register_blueprint(user_blueprint)
