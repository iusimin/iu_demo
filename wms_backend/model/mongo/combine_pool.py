# -*- coding: utf-8 -*-
from datetime import datetime

import mongoengine.fields as f
from bson import ObjectId
from cl.utils.mongo import MongoMixin
from cl.utils.py_enum import PyEnumMixin
from mongoengine import Document, EmbeddedDocument
from wms_backend.model.mongo import IU_DEMO_DB


class CPSortGroupId(EmbeddedDocument, MongoMixin):
    seq_id = f.IntField(db_field="g", required=True)


class CPSortPool(Document, MongoMixin):
    class SortType(PyEnumMixin):
        Combined = 0
        DirectShip = 1

    meta = MongoMixin.NO_INHERIT()
    meta['shard_key'] = False
    meta['index'] = [
        {'keys': 'job_id:1,tracking_id:1', "unique": True},
        {'keys': 'group_ids.seq_id:1'}
    ]

    meta['db_name'] = IU_DEMO_DB
    meta['force_insert'] = True

    job_id = f.StringField(db_field="ji", required=True)
    tracking_id = f.StringField(db_field="ti", required=True)
    sort_type = f.IntField(db_field="st", required=True, choices=SortType.get_ids())
    group_ids = f.ListField(f.EmbeddedDocumentField("CPSortGroupId"), db_field="gs", required=True)

    # parcels in he same cabinet have the same cabinet_id
    cabinet_id = f.StringField(db_field="ci", required=True)
    lattice_id = f.IntField(db_field="li")
    actual_combine_id = f.StringField(db_field="aci")

    created_datetime = f.DateTimeField(db_field="cd", required=True)
    updated_datetime = f.DateTimeField(db_field="ud")

    @classmethod
    def create(cls, job_id, tracking_id, sort_type, group_ids, cabinet_id, lattice_id):
        obj = cls(
            job_id=job_id,
            tracking_id=tracking_id,
            sort_type=sort_type,
            group_ids=group_ids,
            cabinet_id=cabinet_id,
            lattice_id=lattice_id,
            created_datetime=datetime.utcnow()
        )

        obj.save()

    @classmethod
    def by_tracking_id(cls, job_id, tracking_id):
        return cls.find_one({
            "job_id": job_id,
            "tracking_id": tracking_id
        })

    def to_dict(self):
        return self.to_dict_default(date_format='%Y-%m-%d %H:%M:%S')
