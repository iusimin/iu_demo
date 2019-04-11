# -*- coding: utf-8 -*-
from datetime import datetime

from cl.utils.py_enum import PyEnumMixin
from iu_mongo.document import Document, EmbeddedDocument
from iu_mongo.fields import *
from iu_mongo.index import IndexDefinition
from wms_backend.model.mongo import IU_DEMO_DB


class CPSortGroupId(EmbeddedDocument):
    seq_id = IntField(required=True)


class CPSortPool(Document):
    class SortType(PyEnumMixin):
        Combined = 0
        DirectShip = 1

    meta = {
        'indexes': [
            IndexDefinition.parse_from_keys_str("job_id:1,tracking_id:1", unique=True),
            IndexDefinition.parse_from_keys_str("group_ids.seq_id:1")
        ],
        'allow_inheritance': False,
        'db_name': IU_DEMO_DB,
        'force_insert': True,
    }

    job_id = StringField()
    tracking_id = StringField()
    sort_type = IntField()
    group_ids = ListField(EmbeddedDocumentField("CPSortGroupId"))

    # parcels in he same cabinet have the same cabinet_id
    cabinet_id = StringField()
    lattice_id = IntField()
    actual_combine_id = StringField()

    created_datetime = DateTimeField()
    updated_datetime = DateTimeField()

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
