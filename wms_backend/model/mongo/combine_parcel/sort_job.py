# -*- coding: utf-8 -*-
from datetime import datetime

from cl.utils.py_enum import PyEnumMixin
from iu_mongo.document import Document, EmbeddedDocument
from iu_mongo.fields import *
from iu_mongo.index import IndexDefinition
from wms_backend.model.mongo import IU_DEMO_DB
from wms_backend.model.mongo.warehouse_info import CPCabinetSize, CPWarehouse


class CPSortJob(Document):
    class Type(PyEnumMixin):
        CheckInboundParcelReadyToShip = 0
        AllocateCabinetLattice = 1

    meta = {
        'indexes': [
            IndexDefinition.parse_from_keys_str("job_id:1", unique=True),
            IndexDefinition.parse_from_keys_str("job_id:1,warehouse_id:1"),
            IndexDefinition.parse_from_keys_str("job_finish_datetime:1"),
            IndexDefinition.parse_from_keys_str("created_datetime:1,updated_datetime:1")
        ],
        'allow_inheritance': False,
        'db_name': IU_DEMO_DB,
        'force_insert': True,
    }

    job_id = StringField(required=True)
    job_type = IntField(required=True)
    warehouse_id = StringField(required=True)

    warehouse_seed_cabinet_size = EmbeddedDocumentField("CPCabinetSize")
    sort_batch_size = ListField(IntField())
    
    job_finish_datetime = DateTimeField()

    created_datetime = DateTimeField(required=True)
    updated_datetime = DateTimeField()

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
