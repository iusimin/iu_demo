import mongoengine.fields as f
from bson import ObjectId
from mongoengine import Document, EmbeddedDocument

from cl.utils.mongo import MongoMixin
from cl.utils.py_enum import PyEnumMixin
from wms_backend.model.mongo import IU_DEMO_DB
from wms_backend.model.mongo.rbac import Role


class User(Document, MongoMixin):
    meta = {
        'indexes': [
        ],
        'allow_inheritance': False,
        'db_name': IU_DEMO_DB,
        'force_insert': True,
    }

    username = f.StringField(index=True, unique=True)
    password = f.StringField()
    email = f.StringField( index=True, unique=True)
    phone_number = f.StringField()
    permissions = f.ListField(f.EmbeddedDocumentField('Permission'),  default=[])
    role_names = f.ListField(f.StringField(),  default=[])

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
        roles_dict = {r.name: r 
            for r in Role.objects.filter(name__in = self.role_names)}
        return [roles_dict[rn] for rn in self.role_names]

    def to_json_dict(self):
        return {
            'id': str(self.id),
            'username': str(self.username),
            'email': str(self.email),
            'phone_number': str(self.phone_number),
            'role_names': [str(r) for r in self.role_names],
            'permissions_all': [
                p.to_json_dict() for p in self.get_permissions()
            ]
        }
