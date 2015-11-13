# -*- coding:utf-8 -*-
__author__ = 'zeno guo'

from spellworks import db
from datetime import datetime
from utils.database import ModelMixin


Column = db.Column


class Role(db.Model, ModelMixin):
    id = Column(db.Integer, primary_key=True)
    username = Column(db.String(42), nullable=False)
    ip = Column(db.String(42))
    login_date = Column(db.Datetime, default=datetime.utcnow)
