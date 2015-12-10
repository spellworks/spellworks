# -*- coding:utf-8 -*-
__author__ = 'zeno guo'

import re
from spellworks import mail_send
from auth import auth
from auth.models import User, Role
from flask.views import MethodView
from mongoengine.errors import ValidationError
from mongoengine.queryset import NotUniqueError
from flask.ext.login import current_user, login_user, logout_user, login_required
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
            flash(u"Welcome.")
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
        except NotUniqueError, e:  # email or username is not unique
            if re.match(r'.*\$email.*', str(e)):
                return jsonify(status="not-unique", message=u"Email has already confirmed.")
            elif re.match(r'.*\$username.*', str(e)):
                return jsonify(status="not-unique", message=u"Username has already confirmed.")
        except ValidationError, e:  # email or username is invalid
            if re.match(r'.*Mail-address.*', str(e)):
                return jsonify(status="invalid", message=u"Email is invalid.")
            if re.match(r'.*username.*', str(e)):
                return jsonify(status="invalid", message=u"Username is invalid.")
        except ValueError, e:  # password is invalid
            return jsonify(status="invalid", message=u"Password is invalid.")
        except BaseException, e:
            raise e

        login_user(new_user, remember=True)
        token = new_user.generate_token("confirm")
        mail_send.send_email(form['email'], u"注册确认", "/mail/confirm", confirm_token=token)
        flash(u"Welcome, please check your mail box and confirm mail address.")

        return jsonify(status="ok")


class Confirm(MethodView):

    def get(self, confirm_type, token):
        if current_user.is_authenticated and current_user.verify_token(confirm_type, token):
            if confirm_type == "confirm":
                return self._confirm_account()
            else:
                flash(u"Token不合法。")
                return redirect(url_for("main.index"))
        else:
            flash(u"你还没有登录或者token不合法。")
            return redirect(url_for("main.index"))

    def post(self):
        pass

    @staticmethod
    def _confirm_account():
        if current_user.confirmed:
            flash(u"你已经验证过邮箱了。")
        else:
            current_user.confirmed = True
            try:
                current_user.save()
            except BaseException, e:
                raise e
            flash(u"邮箱已经验证成功，欢迎。")
        return redirect(url_for("main.index"))

    @staticmethod
    def _change_email():
        pass

    @staticmethod
    def _reset_password():
        pass


@login_required
def log_out():
    logout_user()
    flash(u"现在你已经注销了。")
    return redirect(url_for("main.index"))
