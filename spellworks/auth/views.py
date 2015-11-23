# -*- coding:utf-8 -*-
__author__ = 'zeno guo'

import re
from auth import auth
from auth.models import User, Role
from flask.views import MethodView
from mongoengine.errors import ValidationError
from mongoengine.queryset import NotUniqueError
from flask.ext.login import current_user, login_user
from flask import url_for, request, redirect, render_template, jsonify, flash


@auth.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping()
    #     if not current_user.confirmed \
    #             and request.endpoint[:5] != 'auth.' \
    #             and request.endpoint != 'static':
    #         return redirect(url_for('auth.unconfirmed'))


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
        if user is not None and user.verify_password(form['password']):
            login_user(user, remember=True)
            flash("Welcome")
        else:
            return jsonify(status="unfind", message=u"Incorrect username or password.")
        return jsonify(status="ok")


class Regist(MethodView):

    def get(self, *args, **kw):
        return redirect(url_for('main.index'))

    def post(self, *args, **kw):
        form = request.form
        try:
            new_user = User(username=form['username'], email=form['email'], role=Role.objects(name="User").first())
            new_user.password = form['password']
            new_user.save()
            login_user(new_user, remember=True)
        except NotUniqueError, e:  # email or username is not unique
            if re.match(r'.*\$email.*', str(e)):
                return jsonify(status="not-unique", message=u"Email has already confirmed.")
            elif re.match(r'.*\$username.*', str(e)):
                return jsonify(status="not-unique", message=u"Username has already confirmed.")
        except ValidationError, e:  # email or username isu invalid
            if re.match(r'.*Mail-address.*', str(e)):
                return jsonify(status="invalid", message=u"Email is invalid.")
            if re.match(r'.*username.*', str(e)):
                return jsonify(status="invalid", message=u"Username is invalid.")
        except ValueError, e:  # password is invalid
            return jsonify(status="invalid", message=u"Password is invalid.")
        except BaseException, e:
            raise e
        return jsonify(status="ok")
