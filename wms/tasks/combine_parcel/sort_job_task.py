import time

from cl.backend.tasks import AbstractAsyncTaskFactory, async_task
from wms.lib.combine_parcel.utilities.sort_job_util import SortJobUtil


class CPSortTasks(AbstractAsyncTaskFactory):
    @async_task(retry_kwargs={
        'max_retries': 1,
    })
    @classmethod
    def run_job(cls, job_id):
        SortJobUtil.allocate_cabinet_for_parcels(job_id)
