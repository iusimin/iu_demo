# -*- coding: utf-8 -*-
import math
from datetime import datetime

from cl.utils.py_enum import PyEnumMixin
from iu_mongo.document import Document, EmbeddedDocument
from iu_mongo.fields import *
from iu_mongo.index import IndexDefinition
from wms.model.mongo import IU_DEMO_DB


class CPSortGroupId(EmbeddedDocument):
    seq_id = IntField(required=True)


class CPSortPool(Document):
    class SortType(PyEnumMixin):
        Combined = 0
        DirectShip = 1

    meta = {
        'indexes': [
            IndexDefinition.parse_from_keys_str("job_id:1,tracking_id:1", unique=True),
            IndexDefinition.parse_from_keys_str("group_ids:1")
        ],
        'allow_inheritance': False,
        'db_name': IU_DEMO_DB,
        'force_insert': True,
    }

    job_id = StringField(required=True)
    tracking_id = StringField(required=True)
    sort_type = IntField(required=True)
    group_ids = ListField(IntField(), required=True)

    # parcels in he same cabinet have the same cabinet_id
    cabinet_id = StringField(required=True)
    lattice_id = IntField(required=True)
    actual_combine_id = StringField()

    created_datetime = DateTimeField(required=True)
    updated_datetime = DateTimeField()

    SORT_GROUP_NAMES = [
        ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q"],
        ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q"],
        ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
    ]

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

    @property
    def group_ids_string(self):
        return "-".join([CPSortPool.SORT_GROUP_NAMES[index][group_id] for index, group_id in enumerate(self.group_ids)] if self.group_ids else [])

    def get_group_id_by_round(self, round_id):
        return CPSortPool.SORT_GROUP_NAMES[round_id][self.group_ids[round_id]]

    def to_dict(self):
        return {
            "tracking_id": self.tracking_id,
            "job_id": self.job_id,
            "cabinet_id": self.cabinet_id,
            "lattice_id": self.lattice_id,
            "sort_type": self.sort_type,
            "group_ids": self.group_ids
        }


class CPSortGroupIdGenerator(object):
    def __init__(self, scale, digits):
        self.scale = scale
        self.digits = digits
        self.count = [0 for x in range(digits)]

    def next(self):
        index = 0
        while index < self.digits:
            if self.count[index] < self.scale - 1:
                self.count[index] += 1
                break
            else:
                self.count[index] = 0
                index += 1

        if index == self.digits:
            raise OverflowError()

    @property
    def current_copy(self):
        return [x for x in self.count]

class CPSortAllocateGroupId(object):
    @staticmethod
    def allocate(items, scale):
        if not scale:
            raise ValueError("scale")
        if not items:
            raise ValueError("items")

        digits = math.ceil(math.log(len(items), scale))
        id_generator = CPSortGroupIdGenerator(scale, digits)

        seq_ids = []

        length = len(items)
        for index, _ in enumerate(items):
            seq_ids.append(id_generator.current_copy)
            if index < length - 1:
                id_generator.next()

        return seq_ids