""" RBAC defination
"""
from mongoengine import Document, EmbeddedDocument
import mongoengine.fields as f
from cl.utils.py_enum import PyEnumMixin
from bson import ObjectId
from web_backend.model.mongo import IU_DEMO_DB
from cl.utils.mongo import MongoMixin
import re

class Permission(EmbeddedDocument, MongoMixin):
    meta = {
        'allow_inheritance': False,
    }
    
    class Action(PyEnumMixin):
        GET = 0
        POST = 1
        PUT = 2
        PATCH = 3
        DELETE = 4

    allow = f.BooleanField(db_field="e")
    resource = f.StringField(db_field="r") # Regex for web endpoint
    actions = f.ListField(f.IntField(choices=Action.get_ids()), db_field="a")

    @classmethod
    def check_permissions(cls, resource, action, permissions, default_allow=False):
        for p in permissions:
            pattern = '^{url_pattern}'.format(
                url_pattern = p.resource
            )
            if re.match(pattern, resource) and (
                    action in p.actions or p.actions == []):
                return p.allow
        else:
            return default_allow
    
    def to_json_dict(self):
        return {
            'allow': self.allow,
            'resource': self.resource,
            'actions': [
                Permission.Action.num_to_name()[a]
                    for a in self.actions
            ]
        }

class Role(Document, MongoMixin):
    meta = {
        'indexes': [
        ],
        'allow_inheritance': False,
        'db_name': IU_DEMO_DB,
        'force_insert': True,
    }

    name = f.StringField(primary_key=True)
    description = f.StringField(db_field="d")
    parents = f.ListField(f.StringField(), db_field="p")
    permissions = f.ListField(f.EmbeddedDocumentField('Permission'), db_field='s')

    def get_permissions(self):
        plist = list(self.permissions)
        parents = Role.objects.filter(name__in = self.parents)
        for r in parents:
            permissions = r.get_permissions()
            for p in permissions:
                if p not in plist:
                    plist.append(p)
        return plist
    
    def to_json_dict(self, fields=None):
        ret = {
            'name': self.name,
            'description': self.description,
            'parents': [str(p) for p in self.parents],
            'permissions': [
                p.to_json_dict() for p in self.permissions
            ],
            'permissions_all': [
                p.to_json_dict() for p in self.get_permissions()
            ]
        }
        if fields is not None:
            ret = {k:v for k, v in ret.items() if k in fields}
        return ret