# -*- coding: utf-8 -*-
from datetime import datetime

from cl.utils.py_enum import PyEnumMixin
from iu_mongo.document import Document, EmbeddedDocument
from iu_mongo.fields import *
from iu_mongo.index import IndexDefinition
from wms.model.mongo import IU_DEMO_DB
from wms.model.mongo.warehouse import CPCabinetSize, CPWarehouse


class CPSortJobTimeline(EmbeddedDocument):
    created = DateTimeField()
    job_started = DateTimeField()
    job_complete = DateTimeField()

class CPSortJob(Document):
    class Type(PyEnumMixin):
        CheckInboundParcelReadyToShip = 0
        AllocateCabinetLattice = 1

    class Status(PyEnumMixin):
        Pending = 0
        Started = 10
        Failed = 99
        Succeeded = 100

    meta = {
        'indexes': [
            {'keys': 'job_id:1', 'unique': True},
            {'keys': 'job_id:1,warehouse_id:1'},
            {'keys': 'warehouse_id:1,job_type:1,status:1'},
            {'keys': 'job_finish_datetime:1'},
            {'keys': 'status:1'}
        ],
        'allow_inheritance': False,
        'db_name': IU_DEMO_DB,
        'force_insert': True,
    }

    job_id = StringField(required=True)
    job_type = IntField(required=True)
    warehouse_id = StringField(required=True)
    status = IntField(required=True)
    timeline = EmbeddedDocumentField("CPSortJobTimeline")

    warehouse_seed_cabinet_size = EmbeddedDocumentField("CPCabinetSize")
    sort_batch_size = IntField(required=True)
    
    job_finish_datetime = DateTimeField()
    failed_reason = StringField()

    created_datetime = DateTimeField(required=True)
    updated_datetime = DateTimeField()

    @classmethod
    def create(cls, job_id, job_type, warehouse_id):
        warehouse = CPWarehouse.by_warehouse_id(warehouse_id)

        if not warehouse:
            raise ValueError("No warehouse with id {0}.".format(warehouse_id))

        utcnow = datetime.utcnow()
        obj = cls(
            job_id=job_id,
            job_type=job_type,
            warehouse_id=warehouse_id,
            status=cls.Status.Pending,
            timeline=CPSortJobTimeline(created=utcnow),
            warehouse_seed_cabinet_size=warehouse.cabinet_size,
            sort_batch_size=warehouse.sort_batch_size,
            created_datetime=utcnow
        )

        obj.save()
        return obj

    @classmethod
    def by_job_id(cls, job_id):
        return cls.find_one({"job_id": job_id})
