# -*- coding:utf-8 -*-
__author__ = 'zeno guo'

from spellworks import db, login_manager
from datetime import datetime
from flask import current_app
from flask.ext.login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


class Permission:
    FOLLOW = 0x01             # 0001
    COMMENT = 0x02            # 0010
    POST = 0x04               # 0100
    WRITE_ARTICLE = 0x08      # 1000
    ADMINISTER = 0x80         # 10000000


TOKEN_TYPE_MAP = ['confirm', 'reset', 'change_email']


class Role(db.Document):
    name = db.StringField(max_length=20, required=True)
    permissions = db.IntField()

    @staticmethod
    def init_roles():
        roles = {
            'User': (Permission.FOLLOW |
                     Permission.COMMENT |
                     Permission.POST,),
            'Member': (Permission.FOLLOW |
                          Permission.COMMENT |
                          Permission.POST |
                          Permission.WRITE_ARTICLE,),
            'Administrator': (0xff,)}
        for r in roles:
            role = Role.objects(name=r).first()
            if role is None:
                role = Role(name=r, permissions=roles[r][0])
                role.save()
            elif role.permissions != roles[r][0]:
                role.permissions = roles[r][0]
                role.save()


class User(UserMixin, db.Document):
    role = db.ReferenceField(Role)
    email = db.EmailField(required=True)
    username = db.StringField(regex=r'[a-zA-Z\_][0-9a-zA-Z\_]*', max_length=42, required=True)
    password_hash = db.StringField(max_length=120)
    comfirmed = db.BooleanField(default=False)
    about_me = db.StringField(max_length=120)
    avatar = db.StringField(max_length=120)
    since = db.DateTimeField(default=datetime.utcnow())
    last_seen = db.DateTimeField(default=datetime.utcnow())
    followed = db.ReferenceField("self", reverse_delete_rule=db.NULLIFY)
    follower = db.ReferenceField("self", reverse_delete_rule=db.NULLIFY)

    @staticmethod
    def hash_password(password):
        return generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_token(self, token_type, expiration=3600):
        if token_type in TOKEN_TYPE_MAP:
            s = Serializer(current_app.config['SECRET_KEY'], expiration)
            return s.dumps({token_type: self.id})

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
        if data.get(token_type) != self.id:
            return False
        return True


@login_manager.user_loader
def load_user(user_id):
    return User.objects(int(user_id)).first()
