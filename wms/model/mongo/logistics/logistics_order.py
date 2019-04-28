# -*- coding: utf-8 -*-
from datetime import datetime

from iu_mongo.document import Document, EmbeddedDocument
from iu_mongo.fields import *

from cl.utils.mongo import MongoMixin
from cl.utils.py_enum import PyEnumMixin
from wms.model.mongo import IU_DEMO_DB
from wms.model.mongo.combine_parcel.operation_record import CPOperationRecord


class LogisticsOrderTimeline(EmbeddedDocument, MongoMixin):
    created = DateTimeField()


class LogisticsOrder(Document, MongoMixin):
    class Status(PyEnumMixin):
        Pending = 0

    meta = {
        'indexes': [
            {'keys': 'tracking_id:1', 'unique': True},
        ],
        'allow_inheritance': False,
        'db_name': IU_DEMO_DB,
        'force_insert': True,
    }

    tracking_id = StringField(required=True)
    platform_id = StringField(required=True)
    carrier_id = StringField(required=True)
    status = IntField(required=True)
    label_url = StringField()

    timeline = EmbeddedDocumentField("LogisticsOrderTimeline")
    operation_records = EmbeddedDocumentListField(
        "CPOperationRecord", default=[])

    weight = FloatField()
    has_battery = BooleanField()
    has_liquid = BooleanField()
    has_sensitive = BooleanField()
    sensitive_reason = StringField()

    created_datetime = DateTimeField(required=True)
    updated_datetime = DateTimeField()

    @classmethod
    def create_if_not_exist(cls, tracking_id, platform_id, carrier_id):
        utcnow = datetime.utcnow()
        obj = cls(
            tracking_id=tracking_id,
            platform_id=platform_id,
            status=cls.Status.Pending,
            carrier_id=carrier_id,
            timeline=LogisticsOrderTimeline(
                created=utcnow
            ),
            created_datetime=utcnow
        )

        obj.save()

        return obj

    @classmethod
    def by_tracking_id(cls, tracking_id):
        return cls.find_one({"tracking_id": tracking_id})

    @classmethod
    def by_tracking_ids(cls, tracking_ids):
        return cls.find({"tracking_id": {"$in": tracking_ids}})

    def to_dict(self):
        return self.to_dict_default(date_format='%Y-%m-%d %H:%M:%S')
