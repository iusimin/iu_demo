# -*- coding: utf-8 -*-

from datetime import datetime

from wms.lib.combine_parcel.data_accessor.combine_pool_accessor import \
    CombinePoolAccessor
from wms.lib.combine_parcel.data_accessor.inbound_parcel_accessor import \
    CPInboundParcelAccessor
from wms.lib.combine_parcel.utilities.combine_pool_util import CombinePoolUtil
from wms.lib.exception.exception import InvalidOperationException
from wms.lib.logistics_order.data_accessor.logistics_order_accessor import \
    LogisticsOrderAccessor
from wms.model.mongo.combine_parcel.combine_pool import CPSortPool
from wms.model.mongo.combine_parcel.combined_logistics_order import \
    CombinedLogisticsOrder
from wms.model.mongo.combine_parcel.operation_record import CPOperationRecord


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
    def inbound_parcel(cls, tracking_id, parcel_type, weight, has_battery, has_liquid, has_sensitive, sensitive_reason, user):
        accessor = CPInboundParcelAccessor(tracking_id)
        accessor.inbound(parcel_type, weight, has_battery,
                         has_liquid, has_sensitive, sensitive_reason)

        accessor.add_operation(
            str(user.id), user.username, CPOperationRecord.CPOperationType.InboundScan, None, None, datetime.utcnow())

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
    def directship_parcel(cls, job_id, tracking_id, weight, user):
        ip_accessor, _, lo_accessor = cls.precheck_directship(
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

        ip_accessor.add_operation(
            str(user.id), user.username, CPOperationRecord.CPOperationType.DirectShip, None, None, datetime.utcnow())

        logistics_order = lo_accessor.order
        return logistics_order

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

    @classmethod
    def combine_parcels(cls, job_id, tracking_ids, weight, user):
        cabinet_id, lattice_id = CombinePoolUtil.check_same_lattice(job_id, tracking_ids)
        combined_logistics_order = CombinedLogisticsOrder.by_cabinet_id_and_lattice_id(cabinet_id, lattice_id)

        if combined_logistics_order:
            logistics_order_id = combined_logistics_order.outbound_logistics_order_id
            accessor = LogisticsOrderAccessor(logistics_order_id)
            has_battery, has_liquid, has_sensitive, sensitive_reason = cls.check_property_of_outbound_logistics_order(tracking_ids)
            accessor.update_parcel_property(weight, has_battery, has_liquid, has_sensitive, sensitive_reason)
            accessor.flush()

            return accessor.order
        else:
            #TODO antony: create logistics order
            pass


    @classmethod
    def check_property_of_outbound_logistics_order(cls, tracking_ids):
        parcels = CPInboundParcelAccessor.by_tracking_ids(tracking_ids)

        has_battery = any([parcel.has_battery for parcel in parcels])
        has_liquid = any([parcel.has_liquid for parcel in parcels])
        has_sensitive = any([parcel.has_sensitive for parcel in parcels])
        sensitive_reason = ",".join([parcel.sensitive_reason for parcel in parcels if parcel.sensitive_reason])

        return has_battery, has_liquid, has_sensitive, sensitive_reason
