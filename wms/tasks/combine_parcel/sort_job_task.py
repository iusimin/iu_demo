# -*- coding: utf-8 -*-

from cl.backend.tasks import AbstractAsyncTaskFactory, async_task
from wms.lib.combine_parcel.utilities.sort_job_util import SortJobUtil


class CPSortJobTasks(AbstractAsyncTaskFactory):
    @classmethod
    @async_task()
    def run_job(cls, task, job_id):
        SortJobUtil.allocate_cabinet_for_parcels(job_id)
