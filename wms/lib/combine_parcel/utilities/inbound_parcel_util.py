# -*- coding: utf-8 -*-

from datetime import datetime

from wms.lib.combine_parcel.data_accessor.inbound_parcel_accessor import \
    CPInboundParcelAccessor
from wms.lib.logistics_order.data_accessor.logistics_order_accessor import \
    LogisticsOrderAccessor


class InboundParcelUtil(object):

    @classmethod
    def create_parcel(cls, tracking_id, combine_id, warehouse_id, inbound_carrier, latest_ship_datetime):
        return CPInboundParcelAccessor.create_if_not_exist(
            tracking_id=tracking_id,
            combine_id=combine_id,
            warehouse_id=warehouse_id,
            inbound_carrier=inbound_carrier,
            latest_ship_datetime=latest_ship_datetime
        )

    @classmethod
    def inbound_parcel(cls, tracking_id, parcel_type, weight, has_battery, has_liquid, has_sensitive, sensitive_reason):
        accessor = CPInboundParcelAccessor(tracking_id)
        accessor.inbound(parcel_type, weight, has_battery, has_liquid, has_sensitive, sensitive_reason)
        accessor.flush()

    @classmethod
    def get_inbound_parcel_detail(cls, tracking_id):
        ip_accessor = CPInboundParcelAccessor(tracking_id)
        parcel = ip_accessor.inbound_parcel
        parcel_dict = parcel.to_dict()
        if parcel.outbound_logistics_order_id:
            lo_accessor = LogisticsOrderAccessor(parcel.outbound_logistics_order_id)
            parcel_dict["outbound_logistics_order"] = lo_accessor.order.to_dict()

        return parcel_dict
