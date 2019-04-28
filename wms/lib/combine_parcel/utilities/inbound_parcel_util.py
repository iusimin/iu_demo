# -*- coding: utf-8 -*-

from datetime import datetime

from wms.lib.combine_parcel.data_accessor.combine_pool_accessor import \
    CombinePoolAccessor
from wms.lib.combine_parcel.data_accessor.inbound_parcel_accessor import \
    CPInboundParcelAccessor
from wms.lib.exception.exception import InvalidOperationException
from wms.lib.logistics_order.data_accessor.logistics_order_accessor import \
    LogisticsOrderAccessor
from wms.model.mongo.combine_parcel.combine_pool import CPSortPool


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
        accessor.inbound(parcel_type, weight, has_battery,
                         has_liquid, has_sensitive, sensitive_reason)
        accessor.flush()

    @classmethod
    def get_inbound_parcel_detail(cls, tracking_id):
        ip_accessor = CPInboundParcelAccessor(tracking_id)
        parcel = ip_accessor.inbound_parcel
        parcel_dict = parcel.to_dict()
        if parcel.outbound_logistics_order_id:
            lo_accessor = LogisticsOrderAccessor(
                parcel.outbound_logistics_order_id)
            parcel_dict["outbound_logistics_order"] = lo_accessor.order.to_dict()

        return parcel_dict

    @classmethod
    def directship_parcel(cls, job_id, tracking_id, weight):
        ip_accessor, cp_accessor, lo_accessor = cls.precheck_directship(
            job_id, tracking_id)

        parcel = ip_accessor.inbound_parcel
        lo_accessor.update_parcel_property(
            weight=weight,
            has_battery=parcel.has_battery,
            has_liquid=parcel.has_liquid,
            has_sensitive=parcel.has_sensitive,
            sensitive_reason=parcel.sensitive_reason
        )
        lo_accessor.flush()
        
        logistics_order = lo_accessor.order
        return logistics_order.label_url

    @classmethod
    def precheck_directship(cls, job_id, tracking_id):
        ip_accessor = CPInboundParcelAccessor(tracking_id)
        parcel = ip_accessor.inbound_parcel

        if not parcel.outbound_logistics_order_id:
            raise InvalidOperationException("非法操作：该订单没有出库物流订单!")
        lo_accessor = LogisticsOrderAccessor(
            parcel.outbound_logistics_order_id)

        cp_accessor = CombinePoolAccessor(job_id, tracking_id)
        sort_info = cp_accessor.sort_info

        if sort_info.sort_type != CPSortPool.SortType.DirectShip:
            raise InvalidOperationException("非法操作：该订单非直发订单！")

        return ip_accessor, cp_accessor, lo_accessor
