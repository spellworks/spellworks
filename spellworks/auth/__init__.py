# -*- coding:utf-8 -*-
__author__ = 'zeno guo'

from flask import Blueprint


auth = Blueprint('auth', __name__)

from auth import views
from auth import urls
