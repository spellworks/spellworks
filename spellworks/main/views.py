# -*- coding:utf-8 -*-
__author__ = 'zeno guo'

from flask.views import MethodView
from flask import jsonify


class Index(MethodView):

    def get(self):
        return "hello, world"

    def post(self, *args, **kw):
        return jsonify(status='ok')
