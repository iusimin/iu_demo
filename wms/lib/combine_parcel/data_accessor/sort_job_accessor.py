
from datetime import datetime

from wms.lib.accessor_base import AccessorBase
from wms.model.mongo.combine_parcel.sort_job import CPSortJob


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
    def has_running_task(cls, job_type, warehouse_id):
        return CPSortJob.find_one({
            "warehouse_id": warehouse_id,
            "job_type": job_type,
            "status": {
                "$in": [CPSortJob.Status.Pending, CPSortJob.Status.Started]
            }
        })

    @classmethod
    def create_if_no_running(cls, job_id, job_type, warehouse_id):
        # TODO: Not atomic, fix later.
        has_running = cls.has_running_task(job_type, warehouse_id)
        job = None
        if not has_running:
            job = CPSortJob.create(job_id, job_type, warehouse_id)

        return job

    @classmethod
    def get_latest_complete_job_id(cls):
        return CPSortJob.find_one(
            {},
            sort=[("job_finish_datetime", -1), ("_id", -1)]
        )

    def start(self):
        self.sort_job.status = CPSortJob.Status.Started
        self.sort_job.timeline.job_started = datetime.utcnow()

    def success(self):
        utcnow = datetime.utcnow()
        self.sort_job.status = CPSortJob.Status.Succeeded
        self.sort_job.timeline.job_complete = utcnow
        self.sort_job.job_finish_datetime = utcnow

    def fail(self, reason):
        utcnow = datetime.utcnow()
        self.sort_job.status = CPSortJob.Status.Failed
        self.sort_job.timeline.job_complete = utcnow
        self.sort_job.job_finish_datetime = utcnow
        self.sort_job.failed_reason = reason

    def flush(self):
        po_props = {
            "status": self.sort_job.status,
            "timeline": self.sort_job.timeline.to_mongo(),
            "job_finish_datetime": self.sort_job.job_finish_datetime,
            "failed_reason": self.sort_job.failed_reason,
            "updated_datetime": datetime.utcnow()
        }

        update_dict = self.split_props(po_props)
        if update_dict:
            self.sort_job.update_one(update_dict)
