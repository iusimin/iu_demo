# -*- coding: utf-8 -*-
from datetime import datetime

from iu_mongo.document import Document, EmbeddedDocument
from iu_mongo.fields import *

from cl.utils.mongo import MongoMixin
from cl.utils.py_enum import PyEnumMixin
from wms.model.mongo import IU_DEMO_DB
from wms.model.mongo.combine_parcel.operation_record import CPOperationRecord


class CombinedLogisticsOrder(Document, MongoMixin):
    meta = {
        'indexes': [
            {'keys': 'cabinet_id:1,lattice_id:1', 'unique': True},
            {'keys': 'outbound_logistics_order_id:1', 'unique': True}
        ],
        'allow_inheritance': False,
        'db_name': IU_DEMO_DB,
        'force_insert': True,
    }

    cabinet_id = StringField(required=True)
    lattice_id = IntField(required=True)
    outbound_logistics_order_id = StringField(required=True)

    @classmethod
    def create_if_not_exist(cls, cabinet_id, lattice_id, outbound_logistics_order_id):
        obj = cls(
            cabinet_id=cabinet_id,
            lattice_id=lattice_id,
            outbound_logistics_order_id=outbound_logistics_order_id
        )

        obj.save()

    @classmethod
    def by_cabinet_id_and_lattice_id(cls, cabinet_id, lattice_id):
        return cls.find_one({
            "cabinet_id": cabinet_id,
            "lattice_id": lattice_id
        })

    @classmethod
    def by_outbound_logistics_order_id(cls, outbound_logistics_order_id):
        return cls.find_one({
            "outbound_logistics_order_id": outbound_logistics_order_id
        })

    def to_dict(self):
        return self.to_dict_default(date_format='%Y-%m-%d %H:%M:%S')