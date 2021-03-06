# -*- coding: utf-8 -*-

from datetime import datetime

from wms.lib.accessor_base import AccessorBase
from wms.model.mongo.logistics.logistics_order import LogisticsOrder


class LogisticsOrderAccessor(AccessorBase):
    def __init__(self, order_id, *args, **kwargs):
        self._order_id = order_id
        self.order = kwargs.get("order")
        if not self.order:
            self.order = LogisticsOrder.by_id(self._order_id)
        super(LogisticsOrderAccessor, self).__init__(*args, **kwargs)

    @classmethod
    def by_tracking_id(cls, tracking_id):
        order = LogisticsOrder.by_tracking_id(tracking_id)
        return cls(order_id=None, order=order)

    @classmethod
    def create_order(cls, tracking_id, platform_id, carrier_id):
        LogisticsOrder.create_if_not_exist(tracking_id, platform_id, carrier_id)

    def update_parcel_property(self, weight, has_battery, has_liquid, has_sensitive, sensitive_reason):
        self.order.weight = weight
        self.order.has_battery = has_battery
        self.order.has_liquid = has_liquid
        self.order.has_sensitive = has_sensitive
        self.order.sensitive_reason = sensitive_reason

    def flush(self, transaction_session=None):
        po_props = {
            "weight": self.order.weight,
            "has_battery": self.order.has_battery,
            "has_liquid": self.order.has_liquid,
            "has_sensitive": self.order.has_sensitive,
            "sensitive_reason": self.order.sensitive_reason,
            "updated_datetime": datetime.utcnow()
        }

        update_dict = self.split_props(po_props)

        if self._operations:
            update_dict["$push"] = {
                "operation_records": {"$each": self._operations}
            }

        if update_dict:
            self.order.update_one(update_dict, session=transaction_session)
