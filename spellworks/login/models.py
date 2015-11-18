# -*- coding:utf-8 -*-
__author__ = 'zeno guo'

from datetime import datetime
from spellworks import db


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


class User(db.Document):
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
