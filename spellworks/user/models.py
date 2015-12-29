# -*- coding:utf-8 -*-
__author__ = 'zeno guo'

import re
from datetime import datetime
from flask.ext.login import UserMixin
from spellworks import db, login_manager
from werkzeug.security import generate_password_hash


class Permission:
    FOLLOW = 0x01             # 0001
    COMMENT = 0x02            # 0010
    POST = 0x04               # 0100
    WRITE_ARTICLE = 0x08      # 1000
    ADMINISTER = 0x80         # 10000000


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
    email = db.EmailField(required=True, unique=True)
    username = db.StringField(regex=r'[a-zA-Z\_][0-9a-zA-Z\_]*', max_length=42, required=True, unique=True)
    password_hash = db.StringField(max_length=120, required=True)
    confirmed = db.BooleanField(default=False)
    about_me = db.StringField(max_length=120)
    avatar = db.StringField(max_length=120)
    since = db.DateTimeField(default=datetime.utcnow())
    last_seen = db.DateTimeField(default=datetime.utcnow())
    followed = db.ReferenceField("self", reverse_delete_rule=db.NULLIFY)
    follower = db.ReferenceField("self", reverse_delete_rule=db.NULLIFY)

    meta = {'allow_inheritance': True}

    def ping(self):
        self.last_seen = datetime.utcnow()
        self.save()

    @staticmethod
    def hash_password(password):
        return generate_password_hash(password)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        if re.match(r'^[\@A-Za-z0-9\!\#\$\%\^\&\*\.\~]{6,22}$', password):
            self.password_hash = generate_password_hash(password)
        else:
            raise ValueError("Password is not valid.")


@login_manager.user_loader
def load_user(user_id):
    return User.objects(id=user_id).first()
