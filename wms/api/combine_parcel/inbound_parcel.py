# -*- coding: utf-8 -*-
import json
from datetime import datetime

import falcon

from cl.backend.api import BaseApiResource
from cl.utils import password
from cl.utils.py_enum import PyEnumMixin
from wms.hooks.auth import login_required, permission_required
from wms.hooks.validation import JsonSchema
from wms.lib.combine_parcel.utilities.inbound_parcel_util import \
    InboundParcelUtil
from wms.lib.exception.exception import InvalidOperationException
from wms.model.mongo.user import User
from wms.model.redis_keys.session import Session


class InboundParcelResource(BaseApiResource):
    class Action(PyEnumMixin):
        inbound = "inbound"
        directship = "directship"

    def __init__(self, *args, **kwargs):
        self._action_map = {
            InboundParcelResource.Action.inbound: self.inbound_parcel,
            InboundParcelResource.Action.directship: self.directship
        }
        super(InboundParcelResource, self).__init__(*args, **kwargs)

    @falcon.before(login_required)
    #@falcon.before(JsonSchema('''
    #type: object
    #properties:
    #  parcel_type: { type: number }
    #  weight: { type: number }
    #  has_battery: { type: boolean }
    #  has_liquid: { type: boolean }
    #  has_sensitive: { type: boolean }
    #required: [parcel_type, weight]
    #'''))
    def on_put(self, req, resp, tracking_id, action):
        action_func = self._action_map.get(action)
        if not action_func:
            raise falcon.HTTPBadRequest("非法操作！")

        session = req.context['session']
        user = session.user
        action_func(req, resp, user, tracking_id)

    def inbound_parcel(self, req, resp, user, tracking_id):
        params = req.media
        parcel_type = params["parcel_type"]
        weight = params["weight"]

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
                sensitive_reason=sensitive_reason,
                user_id=str(user.id),
                operator=user.username
            )
        except ValueError:
            raise falcon.HTTPNotFound(description="物流订单不存在！")
        except InvalidOperationException:
            raise falcon.HTTPBadRequest(description="非法操作!")

    def directship(self, req, resp, user, tracking_id):
        params = req.media
        job_id = params["job_id"]
        weight = params["weight"]
        label_url = InboundParcelUtil.directship_parcel(job_id, tracking_id, weight)

    def on_get(self, req, resp, tracking_id):
        try:
            detail = InboundParcelUtil.get_inbound_parcel_detail(tracking_id)
        except ValueError:
            raise falcon.HTTPNotFound(description="包裹不存在！")

        resp.media = {
            "parcel_detail": detail
        }
