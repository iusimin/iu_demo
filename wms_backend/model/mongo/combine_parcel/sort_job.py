# -*- coding: utf-8 -*-
from datetime import datetime

import mongoengine.fields as f
from bson import ObjectId
from mongoengine import Document, EmbeddedDocument

from cl.utils.mongo import MongoMixin
from cl.utils.py_enum import PyEnumMixin
from wms_backend.model.mongo import IU_DEMO_DB
from wms_backend.model.mongo.warehouse_info import CPCabinetSize, CPWarehouse


class CPSortJob(Document, MongoMixin):
    class Type(PyEnumMixin):
        CheckInboundParcelReadyToShip = 0
        AllocateCabinetLattice = 1

    meta = {
        'indexes': [
            #{'keys': 'job_id:1', "unique": True},
            #{'keys': 'job_id:1,warehouse_id:1'},
            #{'keys': 'job_finish_datetime:1'},
            #{'keys': 'created_datetime:1,updated_datetime:1'},
        ],
        'allow_inheritance': False,
        'db_name': IU_DEMO_DB,
        'force_insert': True,
    }

    job_id = f.StringField()
    job_type = f.IntField()
    warehouse_id = f.StringField()

    warehouse_seed_cabinet_size = f.EmbeddedDocumentField("CPCabinetSize")
    sort_batch_size = f.ListField(f.IntField())
    
    job_finish_datetime = f.DateTimeField()

    created_datetime = f.DateTimeField()
    updated_datetime = f.DateTimeField()

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
