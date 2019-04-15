# -*- coding: utf-8 -*-
import json
from datetime import datetime

import falcon

from cl.utils import password
from wms.api import BaseApiResource
from wms.hooks.auth import login_required, permission_required
from wms.hooks.validation import JsonSchema
from wms.lib.combine_parcel.utilities.inbound_parcel_util import \
    InboundParcelUtil
from wms.lib.exception.exception import InvalidOperationException
from wms.model.mongo.user import User
from wms.model.redis_keys.session import Session


class InboundParcelResource(BaseApiResource):
    @falcon.before(JsonSchema('''
    type: object
    properties:
      tracking_id: { type: string }
      parcel_type: { type: number }
      weight: { type: number }
      has_battery: { type: boolean }
      has_liquid: { type: boolean }
      has_sensitive: { type: boolean }
    required: [tracking_id, parcel_type, weight]
    '''))
    def on_put(self, req, resp):
        params = req.media
        tracking_id = params['tracking_id']
        parcel_type = params['parcel_type']
        weight = params['weight']

        has_battery = params.get("has_battery", False)
        has_liquid = params.get("has_liquid", False)
        has_sensitive = params.get("has_sensitive", False)
        sensitive_reason = params.get("sensitive_reason")

        try:
            InboundParcelUtil.inbound_parcel(
                tracking_id=tracking_id,
                parcel_type=parcel_type,
                weight=weight,
                has_battery=False,#has_battery,
                has_liquid=False,#has_liquid,
                has_sensitive=False,#has_sensitive
            )
        except (ValueError, InvalidOperationException):
            raise falcon.HTTPBadRequest("", "")
