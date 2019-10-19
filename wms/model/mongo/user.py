
# -*- coding: utf-8 -*-

from datetime import datetime

from iu_mongo.document import Document, EmbeddedDocument
from iu_mongo.fields import *

from wms.model.mongo import IU_DEMO_DB
from wms.model.mongo.rbac import Role


class User(Document):
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
    permissions = ListField(EmbeddedDocumentField('Permission'),  default=[])
    role_names = ListField(StringField(),  default=[])

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
        roles_dict = {
            r.name: r for r in Role.find({
                'name': {'$in': self.role_names}
            })
        }
        return [roles_dict[rn] for rn in self.role_names]

    def to_dict(self):
        return {
            'id': str(self.id),
            'username': str(self.username),
            'email': str(self.email),
            'phone_number': str(self.phone_number),
            'role_names': [str(r) for r in self.role_names],
            'permissions_all': [
                p.to_dict() for p in self.get_permissions()
            ],
            'warehouse_id': self.warehouse_id
        }
