# -*- coding:utf-8 -*-
__author__ = 'zeno guo'

from flask.views import MethodView
from flask import jsonify, url_for, request, redirect, render_template
from auth import auth
from auth.models import User
from flask.ext.login import current_user, login_user


@auth.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping()
        if not current_user.confirmed \
                and request.endpoint[:5] != 'auth.' \
                and request.endpoint != 'static':
            return redirect(url_for('auth.unconfirmed'))


@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')


class LoginIndex(MethodView):

    def post(self, *args, **kw):
        form = request.form
        try:
            user = User.objects(email=form.email).first()
        except BaseException, e:
            raise e
        if user is not None and login_user.verify_password(form.password):
            login_user(user)
        else:
            pass  # TODO: flash something!
        return jsonify(status='ok')
