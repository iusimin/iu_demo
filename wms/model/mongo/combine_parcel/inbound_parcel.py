# -*- coding: utf-8 -*-
from datetime import datetime

from iu_mongo.document import Document, EmbeddedDocument
from iu_mongo.fields import *
from iu_mongo.index import IndexDefinition

from cl.utils.mongo import MongoMixin
from cl.utils.py_enum import PyEnumMixin
from wms.model.mongo import IU_DEMO_DB
from wms.model.mongo.combine_parcel.operation_record import CPOperationRecord


class CPInboundParcelTimeline(EmbeddedDocument):
    created = DateTimeField()
    inbound = DateTimeField()
    seeded = DateTimeField()


class CPInboundParcel(Document, MongoMixin):
    class Status(PyEnumMixin):
        Pending = 0
        Inbound = 10
        Sorted = 30
        Seeded = 40
        Combined = 50
        Cancelled = 200

    class ParcelType(PyEnumMixin):
        Ordinary = 0
        Special = 1
        Sensitive = 2

    meta = {
        'indexes': [
            {'keys': 'tracking_id:1', 'unique': True},
            {'keys': 'warehouse_id:1,status:1,ready_to_ship:1,combine_id:1'},
            {'keys': 'timeline.created:1'},
            {'keys': 'timeline.inbound:1'},
            {'keys': 'created_datetime:1'}
        ],
        'allow_inheritance': False,
        'db_name': IU_DEMO_DB,
        'force_insert': True,
    }

    tracking_id = StringField(required=True)
    combine_id = StringField()
    warehouse_id = StringField(required=True)
    inbound_carrier = IntField()
    latest_ship_datetime = DateTimeField(required=True)
    status = IntField(required=True)
    parcel_type = IntField()

    outbound_tracking_id = StringField()

    ready_to_ship = BooleanField()

    timeline = EmbeddedDocumentField("CPInboundParcelTimeline")
    operation_records = EmbeddedDocumentListField("CPOperationRecord", default=[])

    weight = FloatField()
    has_battery = BooleanField()
    has_liquid = BooleanField()
    has_sensitive = BooleanField()
    sensitive_reason = StringField()

    # outbound info

    created_datetime = DateTimeField(required=True)
    updated_datetime = DateTimeField()

    @classmethod
    def create_if_not_exist(cls, tracking_id, combine_id, warehouse_id, inbound_carrier, latest_ship_datetime):
        utcnow = datetime.utcnow()
        obj = cls(
            tracking_id=tracking_id,
            combine_id=combine_id,
            warehouse_id=warehouse_id,
            status=cls.Status.Pending,
            inbound_carrier=inbound_carrier,
            latest_ship_datetime=latest_ship_datetime,
            ready_to_ship=False,
            timeline=CPInboundParcelTimeline(
                created=utcnow
            ),
            created_datetime=utcnow
        )

        obj.save()

        return True, obj

    @classmethod
    def by_tracking_id(cls, tracking_id):
        return cls.find_one({"tracking_id": tracking_id})

    @classmethod
    def by_tracking_ids(cls, tracking_ids):
        return cls.find({"tracking_id": {"$in": tracking_ids}})

    def to_dict(self):
        return self.to_dict_default(date_format='%Y-%m-%d %H:%M:%S')
