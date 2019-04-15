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

    def on_put(self, req, resp):
        tracking_id = req.get_param("tracking_id", required=True)
        parcel_type = req.get_param_as_int("parcel_type", required=True)
        weight = req.get_param_as_int("weight", required=True)

        has_battery = req.get_param_as_bool("has_battery", default=False)
        has_liquid = req.get_param_as_bool("has_liquid", default=False)
        has_sensitive = req.get_param_as_bool("has_sensitive", default=False)

        try:
            InboundParcelUtil.inbound_parcel(
                tracking_id=tracking_id,
                parcel_type=parcel_type,
                weight=weight,
                has_battery=has_battery,
                has_liquid=has_liquid,
                has_sensitive=has_sensitive
            )
        except (ValueError, InvalidOperationException):
            raise falcon.HTTP_BAD_REQUEST()
