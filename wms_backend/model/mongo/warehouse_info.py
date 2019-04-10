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
    meta = {
        'indexes': [
            #{'keys': 'warehouse_id:1', "unique": True}
        ],
        'allow_inheritance': False,
        'db_name': IU_DEMO_DB,
        'force_insert': True,
    }

    warehouse_id = f.StringField()
    cabinet_size = f.EmbeddedDocumentField("CPCabinetSize")

    sort_batch_size = f.ListField(f.IntField())

    created_datetime = f.DateTimeField()
    updated_datetime = f.DateTimeField()

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
