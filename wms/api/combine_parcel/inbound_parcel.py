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
from wms.lib.exception.exception import (InvalidOperationException,
                                         ValidationFailedException)
from wms.model.mongo.user import User
from wms.model.redis_keys.session import Session


class InboundParcelResource(BaseApiResource):
    def on_get(self, req, resp, tracking_id):
        try:
            detail = InboundParcelUtil.get_inbound_parcel_detail(tracking_id)
        except ValueError:
            raise falcon.HTTPNotFound(description="包裹不存在！")

        resp.media = {
            "parcel_detail": detail
        }

    @falcon.before(login_required)
    @falcon.before(JsonSchema('''
    type: object
    properties:
      parcel_type: { type: number }
      weight: { type: number }
      has_battery: { type: boolean }
      has_liquid: { type: boolean }
    required: [parcel_type, weight]
    '''))
    def on_inbound(self, req, resp, tracking_id):
        user = req.context['session'].user

        parcel_type = req.media["parcel_type"]
        weight = req.media["weight"]

        has_battery = req.media.get("has_battery", False)
        has_liquid = req.media.get("has_liquid", False)
        sensitive_reason = req.media.get("sensitive_reason")

        try:
            InboundParcelUtil.inbound_parcel(
                tracking_id=tracking_id,
                parcel_type=parcel_type,
                weight=weight,
                has_battery=has_battery,
                has_liquid=has_liquid,
                has_sensitive=bool(sensitive_reason),
                sensitive_reason=sensitive_reason,
                user=user
            )
        except ValueError:
            raise falcon.HTTPNotFound(description="物流订单不存在！")
        except InvalidOperationException:
            raise falcon.HTTPBadRequest(description="非法操作!")

    @falcon.before(login_required)
    @falcon.before(JsonSchema('''
    type: object
    properties:
      job_id: { type: string }
      weight: { type: number }
    required: [job_id, weight]
    '''))
    def on_directship(self, req, resp, tracking_id):
        user = req.context['session'].user

        job_id = req.media["job_id"]
        weight = req.media["weight"]
        try:
            logistics_order = InboundParcelUtil.directship_parcel(job_id, tracking_id, weight, user)
            resp.media = {
                "logistics_order": logistics_order.to_dict()
            }
        except InvalidOperationException as ex:
            raise falcon.HTTPBadRequest(description=str(ex))

    @falcon.before(login_required)
    @falcon.before(JsonSchema('''
    type: object
    properties:
      job_id: { type: string }
      weight: { type: number }
      tracking_ids: { type: array }
    required: [job_id, weight, tracking_ids]
    '''))
    def on_combine(self, req, resp):
        user = req.context['session'].user

        job_id = req.media["job_id"]
        weight = req.media["weight"]
        tracking_ids = req.media["tracking_ids"]

        try:
            logistics_order = InboundParcelUtil.combine_parcels(job_id, tracking_ids, weight, user)
            resp.media = {
                "logistics_order": logistics_order.to_dict()
            }
        except ValidationFailedException as ex:
            raise falcon.HTTPBadRequest(description=str(ex))
        except InvalidOperationException as ex:
            raise falcon.HTTPBadRequest(description=str(ex))
