
from datetime import datetime

from wms.lib.accessor_base import AccessorBase
from wms.model.mongo.combine_parcel.combine_pool import CPSortPool


class CombinePoolAccessor(AccessorBase):
    def __init__(self, job_id, tracking_id):
        if not tracking_id:
            raise ValueError("tracking_id")
            
        self.sort_info = CPSortPool.by_tracking_id(job_id, tracking_id)

        if not self.sort_info:
            raise ValueError("tracking_id")
