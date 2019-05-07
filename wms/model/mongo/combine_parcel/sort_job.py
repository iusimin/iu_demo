# -*- coding: utf-8 -*-
from datetime import datetime

from iu_mongo.document import Document, EmbeddedDocument
from iu_mongo.fields import *

from cl.utils.mongo import MongoMixin
from cl.utils.py_enum import PyEnumMixin
from wms.model.mongo import IU_DEMO_DB
from wms.model.mongo.combine_parcel.operation_record import CPOperationRecord
from wms.model.mongo.warehouse import CPCabinetSize, Warehouse


class CPSortJobTimeline(EmbeddedDocument, MongoMixin):
    created = DateTimeField()
    job_started = DateTimeField()
    job_complete = DateTimeField()

    def to_dict(self):
        return self.to_dict_default(date_format='%Y-%m-%d %H:%M:%S')


class CPSortJob(Document, MongoMixin):
    class Type(PyEnumMixin):
        CheckInboundParcelReadyToShip = 0
        AllocateCabinetLattice = 1

    class Status(PyEnumMixin):
        Pending = 0
        CalculationStarted = 10
        CalculationComplete = 11
        Cancelled = 98
        Failed = 99
        Succeeded = 100

        _text_dict = {
            Pending: "待运行",
            CalculationStarted: "分拣任务正在生成",
            CalculationComplete: "分拣任务生成完成",
            Cancelled: "取消",
            Failed: "分拣任务失败",
            Succeeded: "分拣播种完成"
        }

        ACTIVESTATUS = [Pending, CalculationStarted, CalculationComplete]

        @classmethod
        def text_dict(cls):
            return cls._text_dict

        @classmethod
        def get_text(cls, status):
            return cls._text_dict[status]

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
    cancel_reason = StringField()

    operation_records = EmbeddedDocumentListField("CPOperationRecord", default=[])

    created_datetime = DateTimeField(required=True)
    updated_datetime = DateTimeField()

    @classmethod
    def create(cls, job_id, job_type, warehouse_id):
        warehouse = Warehouse.by_warehouse_id(warehouse_id)

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

    def to_dict(self):
        return self.to_dict_default(date_format='%Y-%m-%d %H:%M:%S')
