# -*- coding: utf-8 -*-
import json
from datetime import datetime

import falcon

from cl.backend.api import BaseApiResource
from cl.utils import password
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
        sensitive_reason = params.get("sensitive_reason")

        try:
            InboundParcelUtil.inbound_parcel(
                tracking_id=tracking_id,
                parcel_type=parcel_type,
                weight=weight,
                has_battery=has_battery,
                has_liquid=has_liquid,
                has_sensitive=bool(sensitive_reason),
                sensitive_reason=sensitive_reason
            )
        except ValueError:
            raise falcon.HTTPNotFound(description="物流订单不存在！")
        except InvalidOperationException:
            raise falcon.HTTPBadRequest(description="非法操作")
