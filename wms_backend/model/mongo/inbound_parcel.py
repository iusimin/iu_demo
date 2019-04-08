# -*- coding: utf-8 -*-
from datetime import datetime

import mongoengine.fields as f
from bson import ObjectId
from cl.utils.mongo import MongoMixin
from cl.utils.py_enum import PyEnumMixin
from mongoengine import Document, EmbeddedDocument
from wishwms.model.combine_parcel.operation_record import CPOperationRecord
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

    meta = MongoMixin.NO_INHERIT()
    meta['shard_key'] = False
    meta['index'] = [
        {'keys': 'tracking_id:1', "unique": True},
        {'keys': 'warehouse_id:1,status:1,ready_to_ship:1,combine_id:1'},
        {'keys': 'timeline.created:1'},
        {'keys': 'timeline.inbound:1'},
        {'keys': 'created_datetime:1'},
    ]

    meta['db_name'] = IU_DEMO_DB
    meta['force_insert'] = True

    tracking_id = f.StringField(db_field="ti", required=True)
    combine_id = f.StringField(db_field="ci", required=True)
    warehouse_id = f.StringField(db_field="wi", required=True)
    inbound_carrier = f.IntField(db_field="ic")
    latest_ship_datetime = f.DateTimeField(db_field="lot", required=True)
    status = f.IntField(db_field="s", choices=Status.get_ids(), default=Status.Pending, required=True)
    parcel_type = f.IntField(db_field="pt", choices=ParcelType.get_ids())

    outbound_tracking_id = f.StringField(db_field="oti")

    ready_to_ship = f.BooleanField(db_field="rs", required=True, default=False)

    timeline = f.EmbeddedDocumentField("CPInboundParcelTimeline", db_field="tl")
    operation_records = f.ListField(f.EmbeddedDocumentField("CPOperationRecord"), db_field="or", required=True, default=[])

    weight = f.FloatField(db_field='w')
    has_battery = f.BooleanField(db_field='hb', default=False)
    has_liquid = f.BooleanField(db_field='hl', default=False)
    has_sensitive = f.BooleanField(db_field='hs', default=False)

    # outbound info

    created_datetime = f.DateTimeField(db_field="cd", required=True)
    updated_datetime = f.DateTimeField(db_field="ud")

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
