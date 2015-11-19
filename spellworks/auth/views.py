# -*- coding:utf-8 -*-
__author__ = 'zeno guo'

from flask.views import MethodView
from flask import jsonify
import models


class LoginIndex(MethodView):

    def post(self, *args, **kw):
        return jsonify(status='ok')
