from mongoengine import Document, EmbeddedDocument
import mongoengine.fields as f
from cl.utils.py_enum import PyEnumMixin
from bson import ObjectId
from web_backend.model.lib import *

class User(Document):
    meta = {
        'indexes': [
        ],
        'allow_inheritance': False,
        'db_name': WISHPOST_DB,
        'force_insert': True,
    }

    username = f.StringField(db_field="u", index=True, unique=True)
    password = f.StringField(db_field="p")
    email = f.StringField(db_field="e", index=True, unique=True)
    phone_number = f.StringField(db_field="pn")