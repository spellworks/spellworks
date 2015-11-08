# -*- coding:utf-8 -*-
__author__ = 'zeno guo'

from flask import Blueprint


login = Blueprint('login', __name__)

from . import views
from . import urls
