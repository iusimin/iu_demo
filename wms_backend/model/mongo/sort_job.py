# -*- coding: utf-8 -*-
from datetime import datetime

import mongoengine.fields as f
from bson import ObjectId
from cl.utils.mongo import MongoMixin
from cl.utils.py_enum import PyEnumMixin
from mongoengine import Document, EmbeddedDocument
from wms_backend.model.combine_parcel.warehouse_info import (CPCabinetSize,
                                                             CPWarehouse)
from wms_backend.model.mongo import IU_DEMO_DB


class CPSortJob(Document, MongoMixin):
    class Type(PyEnumMixin):
        CheckInboundParcelReadyToShip = 0
        AllocateCabinetLattice = 1

    meta = MongoMixin.NO_INHERIT()
    meta['shard_key'] = False
    meta['index'] = [
        {'keys': 'job_id:1', "unique": True},
        {'keys': 'job_id:1,warehouse_id:1'},
        {'keys': 'job_finish_datetime:1'},
        {'keys': 'created_datetime:1,updated_datetime:1'},
    ]

    meta['db_name'] = IU_DEMO_DB
    meta['force_insert'] = True

    job_id = f.StringField(db_field="ji", required=True)
    job_type = f.IntField(db_field="jt", required=True)
    warehouse_id = f.StringField(db_field="wi", required=True)

    warehouse_seed_cabinet_size = f.EmbeddedDocumentField("CPCabinetSize", db_field="cs", required=True)
    sort_batch_size = f.ListField(f.IntField(), db_field="sz")
    
    job_finish_datetime = f.DateTimeField(db_field="fd")

    created_datetime = f.DateTimeField(db_field="cd", required=True)
    updated_datetime = f.DateTimeField(db_field="ud")

    @classmethod
    def create(cls, job_id, job_type, warehouse_id):
        warehouse = CPWarehouse.by_warehouse_id(warehouse_id)

        if not warehouse:
            raise ValueError("No warehouse with id {0}.".format(warehouse_id))

        obj = cls(
            job_id=job_id,
            job_type=job_type,
            warehouse_id=warehouse_id,
            warehouse_seed_cabinet_size=warehouse.cabinet_size,
            created_datetime=datetime.utcnow()
        )

        obj.save()
        return obj

    @classmethod
    def by_job_id(cls, job_id):
        return cls.find_one({"job_id": job_id})
