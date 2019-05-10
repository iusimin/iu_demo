
from wms.lib.exception.exception import ValidationFailedException
from wms.model.mongo.combine_parcel.combine_pool import CPSortPool


class CombinePoolUtil(object):
    @classmethod
    def check_same_lattice(cls, job_id, tracking_ids):
        parcels = CPSortPool.by_tracking_ids(job_id, tracking_ids)
        if not parcels or len(tracking_ids) != len(tracking_ids):
            raise ValidationFailedException("订单号不存在或不在本job内。")

        cabinet_ids = set([parcel.cabinet_id for parcel in parcels])
        if len(cabinet_ids) > 1:
            raise ValidationFailedException("包裹不属于同一个播种柜。")
        cabinet_id = list(cabinet_ids)[0]

        lattice_ids = set([parcel.lattice_id for parcel in parcels])
        if len(lattice_ids) > 1:
            raise ValidationFailedException("包裹不属于同一个隔口。")
        lattice_id = list(lattice_ids)[0]

        return cabinet_id, lattice_id


