# -*- coding:utf-8 -*-
__author__ = 'zeno guo'

from flask import Blueprint


main = Blueprint('main', __name__)

from . import views
from . import urls
