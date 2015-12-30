# -*- coding:utf-8 -*-
__author__ = 'zeno guo'

from threading import Thread
from flask import current_app, render_template
from flask.ext.mail import Message
from spellworks import mail


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send(to, subject, template, **kwargs):
    app = current_app._get_current_object()
    msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + ' ' + subject,
                  sender=app.config['MAIL_USERNAME'], recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr