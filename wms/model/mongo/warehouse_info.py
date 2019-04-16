# -*- coding: utf-8 -*-
from datetime import datetime

from iu_mongo.document import Document, EmbeddedDocument
from iu_mongo.fields import *
from iu_mongo.index import IndexDefinition
from wms.model.mongo import IU_DEMO_DB


class CPCabinetSize(EmbeddedDocument):
    width = IntField(required=True)
    height = IntField(required=True)


class CPWarehouse(Document):
    meta = {
        'indexes': [
            IndexDefinition.parse_from_keys_str("warehouse_id:1", unique=True)
        ],
        'allow_inheritance': False,
        'db_name': IU_DEMO_DB,
        'force_insert': True,
    }

    warehouse_id = StringField(required=True)
    cabinet_size = EmbeddedDocumentField("CPCabinetSize", required=True)

    sort_batch_size = IntField(required=True)

    created_datetime = DateTimeField(required=True)
    updated_datetime = DateTimeField()

    @classmethod
    def create(cls, warehouse_id, cabinet_width, cabinet_height, sort_batch_size):
        obj = cls(
            warehouse_id=warehouse_id,
            cabinet_size=CPCabinetSize(width=cabinet_width, height=cabinet_height),
            sort_batch_size=sort_batch_size,
            created_datetime=datetime.utcnow()
        )

        obj.save()

    @classmethod
    def by_warehouse_id(cls, warehouse_id):
        return cls.find_one({
            "warehouse_id": warehouse_id
        })
