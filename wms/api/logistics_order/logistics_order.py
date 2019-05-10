# -*- coding: utf-8 -*-
import json
from datetime import datetime

import falcon

from cl.backend.api import BaseApiResource
from cl.utils import password
from wms.hooks.auth import login_required, permission_required
from wms.hooks.validation import JsonSchema
from wms.lib.combine_parcel.utilities.sort_job_util import SortJobUtil
from wms.lib.exception.exception import InvalidOperationException
from wms.lib.logistics_order.data_accessor.logistics_order_accessor import \
    LogisticsOrderAccessor
from wms.lib.logistics_order.utilities.logistics_order_util import \
    LogisticsOrderUtil
from wms.model.mongo.combine_parcel.inbound_parcel import CPInboundParcel


class LogisticsOrder(BaseApiResource):
    @falcon.before(login_required)
    @falcon.before(JsonSchema('''
    type: object
    properties:
      tracking_id: { type: string }
    required: [tracking_id]
    '''))
    def on_get(self, req, resp):
        tracking_id = req.media["tracking_id"]
        