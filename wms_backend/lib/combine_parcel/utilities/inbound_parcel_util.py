# -*- coding: utf-8 -*-

from datetime import datetime

from wishwms.lib.combine_parcel.data_accessor.inbound_parcel_accessor import \
    CPInboundParcelAccessor


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
    def inbound_parcel(cls, tracking_id, parcel_type, weight, has_battery, has_liquid, has_sensitive):
        accessor = CPInboundParcelAccessor(tracking_id)
        accessor.inbound(parcel_type, weight, has_battery, has_liquid, has_sensitive)
        accessor.flush()

    @classmethod
    def check_parcel_ready_to_ship(cls, warehouse_id):
        utcnow = datetime.utcnow()
        parcels_iter = CPInboundParcelAccessor.get_parcels_tobe_combined(warehouse_id)
        expired_parcels = []
        eligible_parcels = []
        combine_ids = set()

        for parcel in parcels_iter:
            combine_ids.add(parcel.combine_id)
            if parcel.latest_ship_datetime <= utcnow:
                expired_parcels.append(parcel)
            else:
                pass


