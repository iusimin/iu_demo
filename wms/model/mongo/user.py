
# -*- coding: utf-8 -*-

from datetime import datetime

from iu_mongo.document import Document, EmbeddedDocument
from iu_mongo.fields import *

from cl.utils.mongo import MongoMixin
from wms.model.mongo import IU_DEMO_DB
from wms.model.mongo.rbac import Role


class User(Document, MongoMixin):
    meta = {
        'indexes': [
            {'keys': 'username:1', 'unique': True},
        ],
        'allow_inheritance': False,
        'db_name': IU_DEMO_DB,
        'force_insert': True,
    }

    username = StringField(required=True)
    password = StringField(required=True)
    email = StringField(required=True)
    phone_number = StringField()
    role_ids = ListField(StringField(), default=[])
    permissions = ListField(EmbeddedDocumentField('Permission'),  default=[])

    warehouse_id = StringField(required=True)

    created_datetime = DateTimeField(required=True)
    updated_datetime = DateTimeField()

    @classmethod
    def create_user(cls, username, password_hashed, email, phone_number, warehouse_id):
        user = User(
            username=username,
            password=password_hashed,
            email=email,
            phone_number=phone_number,
            warehouse_id=warehouse_id,
            created_datetime=datetime.utcnow()
        )

        user.save()
        return user

    @classmethod
    def by_username(cls, username):
        return User.find_one({
            "username": username
        })

    def get_permissions(self):
        plist = list(self.permissions)
        roles = self.get_roles()
        for r in roles:
            permissions = r.get_permissions()
            for p in permissions:
                if p not in plist:
                    plist.append(p)
        return plist
    
    def get_roles(self):
        return Role.by_ids(self.role_ids)

    def to_dict(self):
        return self.to_dict_default(date_format='%Y-%m-%d %H:%M:%S')
