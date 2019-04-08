# -*- coding: utf-8 -*-
from datetime import datetime

import mongoengine.fields as f
from bson import ObjectId
from cl.utils.mongo import MongoMixin
from cl.utils.py_enum import PyEnumMixin
from mongoengine import Document, EmbeddedDocument
from wms_backend.model.mongo import IU_DEMO_DB


class CPCabinetSize(EmbeddedDocument, MongoMixin):
    width = f.IntField(db_field="w", required=True)
    height = f.IntField(db_field="h", required=True)


class CPWarehouse(Document, MongoMixin):
    meta = MongoMixin.NO_INHERIT()
    meta['shard_key'] = False
    meta['index'] = [
        {'keys': 'warehouse_id:1', "unique": True}
    ]

    meta['db_name'] = IU_DEMO_DB
    meta['force_insert'] = True

    warehouse_id = f.StringField(db_field="wi", required=True)
    cabinet_size = f.EmbeddedDocumentField("CPCabinetSize", db_field="cs", required=True)

    sort_batch_size = f.ListField(f.IntField(), db_field="sz")

    created_datetime = f.DateTimeField(db_field="cd", required=True)
    updated_datetime = f.DateTimeField(db_field="ud")

    @classmethod
    def create(cls, warehouse_id, cabinet_width, cabinet_height):
        obj = cls(
            warehouse_id=warehouse_id,
            cabinet_size=CPCabinetSize(width=cabinet_width, height=cabinet_height),
            created_datetime=datetime.utcnow()
        )

        obj.save()

    @classmethod
    def by_warehouse_id(cls, warehouse_id):
        return cls.find_one({
            "warehouse_id": warehouse_id
        })
