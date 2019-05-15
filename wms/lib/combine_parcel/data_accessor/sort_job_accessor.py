
from collections import defaultdict
from datetime import datetime

from wms.lib.accessor_base import AccessorBase
from wms.lib.exception.exception import InvalidOperationException
from wms.model.mongo.combine_parcel.combine_pool import CPSortPool
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
    def get_active_task(cls, job_type, warehouse_id):
        return CPSortJob.find_one({
            "warehouse_id": warehouse_id,
            "job_type": job_type,
            "status": {
                "$in": CPSortJob.Status.ACTIVESTATUS
            }
        })

    @classmethod
    def create_if_no_running(cls, job_id, job_type, warehouse_id):
        # TODO: Not atomic, fix later.
        active_task = cls.get_active_task(job_type, warehouse_id)
        job = None
        if not active_task:
            job = CPSortJob.create(job_id, job_type, warehouse_id)

        return job

    @classmethod
    def get_latest_complete_job_id(cls):
        return CPSortJob.find_one(
            {},
            sort=[("job_finish_datetime", -1), ("_id", -1)]
        )

    @classmethod
    def get_job_parcel_count(cls, job_ids):
        #TODO antony: use aggregation
        parcel_count = defaultdict(int)
        for parcel in CPSortPool.find_iter({
            "job_id": {
                "$in": job_ids
            }
        },
        {
            "job_id": True
        }):
            parcel_count[parcel.job_id] += 1

        return parcel_count

    def check_eligible_to_run(self):
        return self.sort_job.status < CPSortJob.Status.CalculationStarted

    def start_calculation(self):
        if not self.check_eligible_to_run():
            raise InvalidOperationException("该任务已运行！")

        self.sort_job.status = CPSortJob.Status.CalculationStarted
        self.sort_job.timeline.job_started = datetime.utcnow()

    def success(self):
        utcnow = datetime.utcnow()
        self.sort_job.status = CPSortJob.Status.CalculationComplete
        self.sort_job.timeline.job_complete = utcnow
        self.sort_job.job_finish_datetime = utcnow

    def fail(self, reason):
        utcnow = datetime.utcnow()
        self.sort_job.status = CPSortJob.Status.Failed
        self.sort_job.timeline.job_complete = utcnow
        self.sort_job.job_finish_datetime = utcnow
        self.sort_job.failed_reason = reason

    def cancel(self, reason):
        utcnow = datetime.utcnow()
        self.sort_job.status = CPSortJob.Status.Cancelled
        self.sort_job.timeline.job_complete = utcnow
        self.sort_job.job_finish_datetime = utcnow
        self.sort_job.cancel_reason = reason

    def flush(self, transaction_session=None):
        po_props = {
            "status": self.sort_job.status,
            "timeline": self.sort_job.timeline.to_mongo(),
            "job_finish_datetime": self.sort_job.job_finish_datetime,
            "failed_reason": self.sort_job.failed_reason,
            "cancel_reason": self.sort_job.cancel_reason,
            "updated_datetime": datetime.utcnow()
        }

        update_dict = self.split_props(po_props)
        if update_dict:
            self.sort_job.update_one(update_dict, session=transaction_session)
