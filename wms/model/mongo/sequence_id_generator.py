# -*- coding: utf-8 -*-

from iu_mongo.document import Document, EmbeddedDocument
from iu_mongo.fields import *
from iu_mongo.index import IndexDefinition
from wms.model.mongo import IU_DEMO_DB


class SequenceIdGenerator(Document):
    '''
        Generate sequence id with format: {prefix}-{current_number}.
        current_number will increase by one automatically.
    '''
    meta = {
        'indexes': [
            IndexDefinition.parse_from_keys_str("prefix:1", unique=True)
        ],
        'allow_inheritance': False,
        'db_name': IU_DEMO_DB,
        'force_insert': True,
    }

    prefix = StringField(required=True)
    current_number = IntField(required=True)

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
