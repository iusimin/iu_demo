# -*- coding: utf-8 -*-

from cl.backend.tasks import AbstractAsyncTaskFactory, async_task
from wms.lib.combine_parcel.utilities.sort_job_util import SortJobUtil


class CPSortJobTasks(AbstractAsyncTaskFactory):
    @classmethod
    @async_task()
    def run_allocate_cabinet_job(cls, task, job_id):
        SortJobUtil.allocate_cabinet_for_parcels(job_id)

    @classmethod
    @async_task()
    def run_check_ready_to_ship_job(cls, task, job_id):
        SortJobUtil.check_inbound_parcel_ready_to_ship(job_id)
