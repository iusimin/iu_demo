# -*- coding: utf-8 -*-
from datetime import datetime

from iu_mongo.document import Document, EmbeddedDocument
from iu_mongo.fields import *

from cl.utils.mongo import MongoMixin
from cl.utils.py_enum import PyEnumMixin
from wms.model.mongo import IU_DEMO_DB


class CPCabinetSize(EmbeddedDocument, MongoMixin):
    width = IntField(required=True)
    height = IntField(required=True)

    def to_dict(self):
        return self.to_dict_default(date_format='%Y-%m-%d %H:%M:%S')


class Warehouse(Document, MongoMixin):
    class WeightUnit(PyEnumMixin):
        Gram = 0
        Kilogram = 1

        _text_dict = {
            Gram: "克",
            Kilogram: "千克"
        }

        @classmethod
        def text_dict(cls):
            return cls._text_dict

        @classmethod
        def get_text(cls, status):
            return cls._text_dict[status]

    class CabinetOrientation(PyEnumMixin):
        Horizontal = 0
        Vertical = 1

        _text_dict = {
            Horizontal: "横向",
            Vertical: "竖向"
        }

        @classmethod
        def text_dict(cls):
            return cls._text_dict

        @classmethod
        def get_text(cls, status):
            return cls._text_dict[status]

    meta = {
        'indexes': [
            {'keys': 'warehouse_id:1', 'unique': True}
        ],
        'allow_inheritance': False,
        'db_name': IU_DEMO_DB,
        'force_insert': True,
    }

    warehouse_id = StringField(required=True)
    warehouse_name = StringField(required=True)
    cabinet_count = IntField(required=True)
    cabinet_size = EmbeddedDocumentField("CPCabinetSize", required=True)
    cabinet_orientation = IntField()

    sort_batch_size = IntField(required=True)
    weight_unit = IntField()

    created_datetime = DateTimeField(required=True)
    updated_datetime = DateTimeField()

    @classmethod
    def create(cls, warehouse_id, warehouse_name, cabinet_count, cabinet_width, cabinet_height, sort_batch_size):
        obj = cls(
            warehouse_id=warehouse_id,
            warehouse_name=warehouse_name,
            cabinet_count=cabinet_count,
            cabinet_size=CPCabinetSize(
                width=cabinet_width, height=cabinet_height),
            sort_batch_size=sort_batch_size,
            created_datetime=datetime.utcnow()
        )

        obj.save()

    @classmethod
    def by_warehouse_id(cls, warehouse_id):
        return cls.find_one({
            "warehouse_id": warehouse_id
        })

    def to_dict(self):
        return self.to_dict_default(date_format='%Y-%m-%d %H:%M:%S')
