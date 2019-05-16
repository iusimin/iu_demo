""" RBAC defination
"""
from iu_mongo import Document, EmbeddedDocument
import iu_mongo.fields as f
from cl.utils.py_enum import PyEnumMixin
from bson import ObjectId
from cl.utils.mongo import MongoMixin
import re

class Permission(EmbeddedDocument, MongoMixin):
    class Action(PyEnumMixin):
        GET = 0
        POST = 1
        PUT = 2
        PATCH = 3
        DELETE = 4

    allow = f.BooleanField()
    resource = f.StringField() # Regex for web endpoint
    actions = f.ListField(f.IntField(choices=Action.get_ids()))

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
        'db_name': 'iu-demo',
    }

    name = f.StringField()
    description = f.StringField()
    parents = f.ListField(f.StringField())
    permissions = f.ListField(f.EmbeddedDocumentField('Permission'))

    def get_permissions(self):
        plist = list(self.permissions)
        parents = Role.find({
            'name': {
                '$in': self.parents,
            }
        })
        for r in parents:
            permissions = r.get_permissions()
            for p in permissions:
                if p not in plist:
                    plist.append(p)
        return plist
    
    def to_json_dict(self):
        ret = {
            'name': self.name,
            'description': self.description,
            'parents': [str(p) for p in self.parents],
            'created_ts': self.id.generation_time.strftime('%Y-%m-%d %H:%M:%S'),
            'permissions': [
                p.to_json_dict() for p in self.permissions
            ],
            'permissions_all': [
                p.to_json_dict() for p in self.get_permissions()
            ]
        }
        return ret