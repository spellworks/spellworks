# -*- coding:utf-8 -*-
__author__ = 'zeno guo'

from flask.views import MethodView
from flask import jsonify
# from . import models
from main import views


class LoginIndex(MethodView):

    def get(self):
        return "hello, world"

    def post(self, *args, **kw):
        return jsonify(status='ok')
