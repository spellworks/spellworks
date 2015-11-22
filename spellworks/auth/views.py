# -*- coding:utf-8 -*-
__author__ = 'zeno guo'

import re
from auth import auth
from auth.models import User
from flask.views import MethodView
from mongoengine.errors import ValidationError
from mongoengine.queryset import NotUniqueError
from flask.ext.login import current_user, login_user
from flask import url_for, request, redirect, render_template, jsonify, flash


@auth.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping()
        if not current_user.confirmed \
                and request.endpoint[:5] != 'auth.' \
                and request.endpoint != 'static':
            return redirect(url_for('auth.unconfirmed'))


def unconfirmed():
    if not current_user.is_anonymous and current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')


class Login(MethodView):

    def get(self, *args, **kw):
        return redirect(url_for('main.index'))

    def post(self, *args, **kw):
        form = request.form
        try:
            if u'@' in form['username']:
                user = User.objects(email=form['username']).first()
            else:
                user = User.objects(username=form['username']).first()
        except BaseException, e:
            raise e
            user = None
        if user is not None and login_user.verify_password(form['password']):
            login_user(user, remember=True)
            flash("Welcome")
        else:
            return jsonify(status="unfind")
        return jsonify(status="ok")


class Regist(MethodView):

    def get(self, *args, **kw):
        return redirect(url_for('main.index'))

    def post(self, *args, **kw):
        form = request.form
        try:
            new_user = User(username=form['username'], email=form['email'])
            new_user.password = form['password']
            new_user.save()
        except NotUniqueError, e:  # email or username is not unique
            if re.match(r'.*/$email.*', str(e)):
                pass
            elif re.match(r'.*/$username.*', str(e)):
                pass
        except ValidationError, e:  # email or username is invalid
            pass
        except ValueError, e:  # password is invalid
            pass
        except BaseException, e:
            raise e
