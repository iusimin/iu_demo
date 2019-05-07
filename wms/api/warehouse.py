# -*- coding: utf-8 -*-
import json
from datetime import datetime

import falcon

from cl.backend.api import BaseApiResource
from wms.hooks.auth import login_required, permission_required
from wms.hooks.validation import JsonSchema
from wms.lib.common.data_accessor.warehouse_accessor import WarehouseAccessor


class Warehouse(BaseApiResource):
    @falcon.before(login_required)
    def on_get(self, req, resp, warehouse_id):
        accessor = WarehouseAccessor(warehouse_id)
        warehouse = accessor.warehouse

        resp.media = {
            "warehouse": warehouse.to_dict()
        }


class OperatorWarehouse(BaseApiResource):
    @falcon.before(login_required)
    def on_get(self, req, resp):
        session = req.context['session']
        user = session.user
        warehouse_id = user.warehouse_id
        accessor = WarehouseAccessor(warehouse_id)
        warehouse = accessor.warehouse

        resp.media = {
            "warehouse": warehouse.to_dict()
        }

    @falcon.before(login_required)
    @falcon.before(JsonSchema('''
    type: object
    properties:
      warehouse_id: { type: string }
      cabinet_count: { type: number }
      cabinet_size: { type: object }
      cabinet_orientation: { type: number }
      weight_unit: { type: number }
    required: [warehouse_id, cabinet_count, cabinet_size, cabinet_orientation, weight_unit]
    '''))
    def on_put(self, req, resp):
        warehouse_id = req.media["warehouse_id"]
        cabinet_count = req.media["cabinet_count"]
        cabinet_orientation = req.media["cabinet_orientation"]
        cabinet_size = req.media["cabinet_size"]
        weight_unit = req.media["weight_unit"]

        accessor = WarehouseAccessor(warehouse_id)
        accessor.update_setting(
            cabinet_count=cabinet_count,
            cabinet_size=cabinet_size,
            cabinet_orientation=cabinet_orientation,
            weight_unit=weight_unit)

        accessor.flush()
