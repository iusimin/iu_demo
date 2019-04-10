
from datetime import datetime

from wms_backend.lib.accessor_base import AccessorBase
from wms_backend.model.mongo.combine_parcel.sort_job import CPSortJob


class SortJobAccessor(AccessorBase):
    def __init__(self, job_id, *args, **kwargs):
        if not job_id:
            raise ValueError("job_id is null or empty.")

        self._job_id = job_id
        self.sort_job = CPSortJob.by_job_id(self._job_id)

        if not self.sort_job:
            raise ValueError("Job with id {0} doesn't exist.".format(job_id))

        super(SortJobAccessor, self).__init__(*args, **kwargs)

    @classmethod
    def create(cls, job_id, job_type, warehouse_id):
        return CPSortJob.create(job_id, job_type, warehouse_id)

    @classmethod
    def get_latest_complete_job_id(cls):
        return CPSortJob.find_one(
            {},
            sort=[("job_finish_datetime", -1), ("_id", -1)]
        )

    def finish(self):
        self.sort_job.job_finish_datetime = datetime.utcnow()

    def flush(self):
        po_props = {
            "job_finish_datetime": self.sort_job.job_finish_datetime,
            "updated_datetime": datetime.utcnow()
        }

        update_dict = self.split_props(po_props)
        if update_dict:
            self.sort_job.update_one(update_dict)
