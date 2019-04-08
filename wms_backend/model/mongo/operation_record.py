# -*- coding: utf-8 -*-
from datetime import datetime

import mongoengine.fields as f
from bson import ObjectId
from cl.utils.mongo import MongoMixin
from cl.utils.py_enum import PyEnumMixin
from mongoengine import Document, EmbeddedDocument
from wms_backend.model.mongo import IU_DEMO_DB


class CPOperationRecord(EmbeddedDocument, MongoMixin):
    class CPOperationType(PyEnumMixin):
        InboundScan = 0

    operator = f.StringField(db_field="o", required=True)
    operation = f.IntField(db_field="op", required=True)
    operation_description = f.StringField(db_field="opd", required=True)
    operation_info = f.DictField(db_field="oi")
    operation_datetime = f.DateTimeField(db_field="cd", required=True)
    