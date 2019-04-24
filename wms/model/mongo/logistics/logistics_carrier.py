# -*- coding: utf-8 -*-
from datetime import datetime

from iu_mongo.document import Document, EmbeddedDocument
from iu_mongo.fields import *

from cl.utils.mongo import MongoMixin
from cl.utils.py_enum import PyEnumMixin
from wms.model.mongo import IU_DEMO_DB



class LogisticsCarrier(Document, MongoMixin):
    class Status(PyEnumMixin):
        Pending = 0
        Enabled = 10
        Disabled = 100

    meta = {
        'indexes': [
            {'keys': 'carrier_name:1', 'unique': True},
        ],
        'allow_inheritance': False,
        'db_name': IU_DEMO_DB,
        'force_insert': True,
    }

    carrier_name = StringField(required=True)
    carrier_name_chs = StringField(required=True)
    status = IntField(required=True)

    created_datetime = DateTimeField(required=True)
    updated_datetime = DateTimeField()

    @classmethod
    def create_if_not_exist(cls, carrier_name, carrier_name_chs):
        utcnow = datetime.utcnow()
        obj = cls(
            carrier_name=carrier_name,
            carrier_name_chs=carrier_name_chs,
            status=cls.Status.Pending,
            created_datetime=utcnow
        )

        obj.save()

        return obj

    def to_dict(self):
        return self.to_dict_default(date_format='%Y-%m-%d %H:%M:%S')
