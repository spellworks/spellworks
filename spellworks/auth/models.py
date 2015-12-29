# -*- coding:utf-8 -*-
__author__ = 'zeno guo'

from flask import current_app
from spellworks.user.models import User
from werkzeug.security import check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


class Permission:
    FOLLOW = 0x01             # 0001
    COMMENT = 0x02            # 0010
    POST = 0x04               # 0100
    WRITE_ARTICLE = 0x08      # 1000
    ADMINISTER = 0x80         # 10000000


TOKEN_TYPE_MAP = ['confirm', 'reset', 'change_email']


class AuthUser(User):

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_token(self, token_type, expiration=3600):
        if token_type in TOKEN_TYPE_MAP:
            s = Serializer(current_app.config['SECRET_KEY'], expiration)
            return s.dumps({token_type: str(self.id)})

    def verify_token(self, token_type, token):
        if token_type not in TOKEN_TYPE_MAP:
            return False
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if token_type not in data:
            return False
        if data.get(token_type) != str(self.id):
            return False
        return True
