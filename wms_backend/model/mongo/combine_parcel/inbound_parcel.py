# -*- coding: utf-8 -*-
from datetime import datetime

import mongoengine.fields as f
from bson import ObjectId
from cl.utils.mongo import MongoMixin
from cl.utils.py_enum import PyEnumMixin
from mongoengine import Document, EmbeddedDocument
from wms_backend.model.mongo.combine_parcel.operation_record import CPOperationRecord
from wms_backend.model.mongo import IU_DEMO_DB


class CPInboundParcelTimeline(EmbeddedDocument, MongoMixin):
    created = f.DateTimeField(db_field="c")
    inbound = f.DateTimeField(db_field="i")
    seeded = f.DateTimeField(db_field="s")


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
            #{'keys': 'tracking_id:1', "unique": True},
            #{'keys': 'warehouse_id:1,status:1,ready_to_ship:1,combine_id:1'},
            #{'keys': 'timeline.created:1'},
            #{'keys': 'timeline.inbound:1'},
            #{'keys': 'created_datetime:1'},
        ],
        'allow_inheritance': False,
        'db_name': IU_DEMO_DB,
        'force_insert': True,
    }

    tracking_id = f.StringField()
    combine_id = f.StringField()
    warehouse_id = f.StringField()
    inbound_carrier = f.IntField()
    latest_ship_datetime = f.DateTimeField()
    status = f.IntField()
    parcel_type = f.IntField()

    outbound_tracking_id = f.StringField()

    ready_to_ship = f.BooleanField()

    timeline = f.EmbeddedDocumentField("CPInboundParcelTimeline")
    operation_records = f.ListField(f.EmbeddedDocumentField("CPOperationRecord"), default=[])

    weight = f.FloatField()
    has_battery = f.BooleanField()
    has_liquid = f.BooleanField()
    has_sensitive = f.BooleanField()

    # outbound info

    created_datetime = f.DateTimeField()
    updated_datetime = f.DateTimeField()

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

        try:
            obj.save()
        except OperationError as ex:
            if 'duplicate unique keys' in ex.message:
                return False, None
            else:
                raise

        return True, obj

    @classmethod
    def by_tracking_id(cls, tracking_id):
        return cls.find_one({"tracking_id": tracking_id})

    @classmethod
    def by_tracking_ids(cls, tracking_ids):
        return cls.find({"tracking_id": {"$in": tracking_ids}})

    def to_dict(self):
        return self.to_dict_default(date_format='%Y-%m-%d %H:%M:%S')
