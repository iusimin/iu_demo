# -*- coding: utf-8 -*-

import mongoengine.fields as f
from mongoengine import Document, OperationError

from cl.utils.mongo import MongoMixin
from cl.utils.py_enum import PyEnumMixin
from wms_backend.model.mongo import IU_DEMO_DB


class SequenceIdGenerator(MongoMixin, Document):
    '''
        Generate sequence id with format: {prefix}-{current_number}.
        current_number will increase by one automatically.
    '''
    meta = MongoMixin.NO_INHERIT()
    meta['shard_key'] = False
    meta['index'] = [
        {'keys': "prefix:1", "unique": True}
    ]

    meta['db_name'] = IU_DEMO_DB
    meta['force_insert'] = True

    prefix = f.StringField(db_field="p", required=True)
    current_number = f.IntField(db_field="c", required=True)

    @classmethod
    def get_sequence_id(cls, prefix, number_digits=5):
        obj = cls._get_or_create(prefix)
        obj.inc(current_number=1)
        return "{0}-{1}".format(
            obj.prefix, str(obj.current_number).zfill(number_digits))

    @classmethod
    def get_sequence_number(cls, prefix, step=1, start_number=0):
        obj = cls._get_or_create(prefix, start_number=start_number)
        obj.inc(current_number=step)
        return obj.current_number

    @classmethod
    def _get_or_create(cls, prefix, start_number=0):
        obj = cls.find_one({"prefix": prefix})
        if not obj:
            obj = cls(
                prefix=prefix,
                current_number=start_number
            )
            try:
                obj.save()
            except OperationError as ex:
                if 'duplicate unique keys' in ex.message:
                    obj = cls.find_one({"prefix": prefix})
                else:
                    raise
        return obj
