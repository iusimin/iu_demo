# -*- coding: utf-8 -*-
import functools
from datetime import datetime

from wms_backend.lib.accessor_base import AccessorBase
from wms_backend.lib.exception.exception import InvalidOperationException
from wms_backend.model.mongo.combine_parcel.inbound_parcel import CPInboundParcel


class CPInboundParcelAccessor(AccessorBase):
    class StatusChecker(object):
        def __init__(self, white_list):
            self._white_list = white_list

        def __call__(self, func):
            def wrapper(*args, **kwargs):
                accessor = args[0]
                if accessor.inbound_parcel.status not in self._white_list:
                    raise InvalidOperationException("Operation is not allowed in status {0}.".format(accessor.inbound_parcel.status))

                return func(*args, **kwargs)

            return wrapper


    def __init__(self, tracking_id, *args, **kwargs):
        if not tracking_id:
            raise ValueError("tracking_id is null or empty.")

        self._tracking_id = tracking_id
        self.inbound_parcel = CPInboundParcel.by_tracking_id(self._tracking_id)

        if not self.inbound_parcel:
            raise ValueError("Parcel with tracking id {0} doesn't exist.".format(tracking_id))

        super(CPInboundParcelAccessor, self).__init__(*args, **kwargs)

    @classmethod
    def create_if_not_exist(cls, tracking_id, combine_id, warehouse_id, inbound_carrier, latest_ship_datetime):
        CPInboundParcel.create_if_not_exist(
            tracking_id=tracking_id,
            combine_id=combine_id,
            warehouse_id=warehouse_id,
            inbound_carrier=inbound_carrier,
            latest_ship_datetime=latest_ship_datetime
        )

    @classmethod
    def get_parcels_tobe_combined(cls, warehouse_id):
        return CPInboundParcel.find_iter({
            "warehouse_id": warehouse_id,
            "status": {
                "$in": [CPInboundParcel.Status.Pending, CPInboundParcel.Status.Inbound]
            },
            "ready_to_ship": False
        })

    @StatusChecker([CPInboundParcel.Status.Pending, CPInboundParcel.Status.Inbound, CPInboundParcel.Status.Sorted, CPInboundParcel.Status.Combined])
    def inbound(self, parcel_type, weight, has_battery, has_liquid, has_sensitive):
        self.inbound_parcel.parcel_type = parcel_type
        self.inbound_parcel.weight = weight
        self.inbound_parcel.has_battery = has_battery
        self.inbound_parcel.has_liquid = has_liquid
        self.inbound_parcel.has_sensitive = has_sensitive
        self.inbound_parcel.status = CPInboundParcel.Status.Inbound
        self.inbound_parcel.timeline.inbound = datetime.utcnow()

    def flush(self):
        po_props = {
            "status": self.inbound_parcel.status,
            "weight": self.inbound_parcel.weight,
            "has_battery": self.inbound_parcel.has_battery,
            "has_liquid": self.inbound_parcel.has_liquid,
            "has_sensitive": self.inbound_parcel.has_sensitive,
            "timeline": self.inbound_parcel.timeline,
            "updated_datetime": datetime.utcnow()
        }

        update_dict = self.split_props(po_props)

        if self._operations:
            update_dict["$push"] = {
                "operation_records": {"$each": self._operations}
            }

        if update_dict:
            self.inbound_parcel.update_one(update_dict)
