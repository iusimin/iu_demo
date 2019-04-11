# -*- coding: utf-8 -*-
from datetime import datetime

from cl.utils.py_enum import PyEnumMixin
from iu_mongo.document import Document, EmbeddedDocument
from iu_mongo.fields import *
from iu_mongo.index import IndexDefinition
from wms.model.mongo import IU_DEMO_DB


class CPOperationRecord(EmbeddedDocument):
    class CPOperationType(PyEnumMixin):
        InboundScan = 0

    operator = StringField()
    operation = IntField()
    operation_description = StringField()
    operation_info = DictField()
    operation_datetime = DateTimeField()
