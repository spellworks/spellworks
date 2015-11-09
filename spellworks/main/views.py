# -*- coding:utf-8 -*-
__author__ = 'zeno guo'

from flask.views import MethodView
from flask import jsonify, render_template


class Index(MethodView):

    def get(self):
        return render_template('test.html')

    def post(self, *args, **kw):
        return jsonify(status='ok')
