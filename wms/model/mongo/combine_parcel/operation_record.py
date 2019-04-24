# -*- coding: utf-8 -*-
from datetime import datetime

from iu_mongo.document import Document, EmbeddedDocument
from iu_mongo.fields import *

from cl.utils.mongo import MongoMixin
from cl.utils.py_enum import PyEnumMixin
from wms.model.mongo import IU_DEMO_DB


class CPOperationRecord(EmbeddedDocument, MongoMixin):
    class CPOperationType(PyEnumMixin):
        InboundScan = 0

    operator = StringField()
    operation = IntField()
    operation_description = StringField()
    operation_info = DictField()
    operation_datetime = DateTimeField()

    def to_dict(self):
        return self.to_dict_default(date_format='%Y-%m-%d %H:%M:%S')
