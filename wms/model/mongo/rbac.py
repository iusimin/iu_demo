""" RBAC defination
"""
import re

from bson import ObjectId
from iu_mongo.document import Document, EmbeddedDocument
from iu_mongo.fields import *

from cl.utils.mongo import MongoMixin
from cl.utils.py_enum import PyEnumMixin
from wms.model.mongo import IU_DEMO_DB


class Permission(EmbeddedDocument, MongoMixin):
    class Action(PyEnumMixin):
        GET = 0
        POST = 1
        PUT = 2
        PATCH = 3
        DELETE = 4

    allow = BooleanField()
    resource = StringField() # Regex for web endpoint
    actions = ListField(IntField())

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
    
    def to_dict(self):
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
            {'keys': 'name:1', 'unique': True},
        ],
        'db_name': IU_DEMO_DB,
    }

    name = StringField()
    description = StringField()
    parents = ListField(StringField())
    permissions = ListField(EmbeddedDocumentField('Permission'))

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
    
    def to_dict(self, fields=None):
        return self.to_dict_default(date_format='%Y-%m-%d %H:%M:%S')
