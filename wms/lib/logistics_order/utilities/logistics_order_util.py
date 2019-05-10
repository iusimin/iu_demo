# -*- coding: utf-8 -*-

from wms.lib.combine_parcel.utilities.inbound_parcel_util import \
    InboundParcelUtil
from wms.lib.logistics_order.data_accessor.logistics_order_accessor import \
    LogisticsOrderAccessor


class LogisticsOrderUtil(object):
    @classmethod
    def outbound_scan(cls, tracking_id, weight):
        pass