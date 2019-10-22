# -*- coding: UTF-8 -*-

from wms.server import ConfigParser, IUWMSBackendService
from wms.model.mongo.combine_parcel.sort_job import CPSortJob
from wms.model.mongo.warehouse import Warehouse

from wms.tasks.combine_parcel.sort_job_task import CPSortJobTasks

CONFIG_FILE = '/etc/server.yml'

def _setup():
    options = ConfigParser.parse_config_file(CONFIG_FILE)
    options['rate-limiter']['enable'] = False
    application = IUWMSBackendService(options)
    application.connect()

def run():
    jobs = CPSortJob.find_iter({
        "status": CPSortJob.Status.Pending
    })
    for job in jobs:
        if job.job_type == CPSortJob.Type.AllocateCabinetLattice:
            CPSortJobTasks.run_allocate_cabinet_job(job.job_id)
        elif job.job_type == CPSortJob.Type.CheckInboundParcelReadyToShip:
            CPSortJobTasks.run_check_ready_to_ship_job(job.job_id)


if __name__ == "__main__":
    _setup()
    run()
