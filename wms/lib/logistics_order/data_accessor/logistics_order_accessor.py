# -*- coding: utf-8 -*-

from wms.lib.accessor_base import AccessorBase
from wms.model.mongo.logistics.logistics_order import LogisticsOrder


class LogisticsOrderAccessor(AccessorBase):
    def __init__(self, order_id):
        self._order_id = order_id
        self.order = LogisticsOrder.by_id(self._order_id)

    @classmethod
    def create_order(cls, tracking_id, platform_id, carrier_id):
        LogisticsOrder.create_if_not_exist(tracking_id, platform_id, carrier_id)
