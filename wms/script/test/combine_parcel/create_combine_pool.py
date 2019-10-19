# -*- coding: UTF-8 -*-

import random
from collections import defaultdict
from datetime import datetime, timedelta

from bson import ObjectId

from wms.lib.combine_parcel.data_accessor.combine_pool_accessor import \
    CombinePoolAccessor
from wms.lib.combine_parcel.data_accessor.inbound_parcel_accessor import \
    CPInboundParcelAccessor
from wms.lib.combine_parcel.data_accessor.sort_job_accessor import \
    SortJobAccessor
from wms.lib.combine_parcel.utilities.inbound_parcel_util import \
    InboundParcelUtil
from wms.model.mongo.combine_parcel.combine_pool import (CPSortAllocateGroupId,
                                                         CPSortPool)
from wms.model.mongo.combine_parcel.inbound_parcel import CPInboundParcel
from wms.model.mongo.combine_parcel.sort_job import CPSortJob
from wms.model.mongo.sequence_id_generator import SequenceIdGenerator
from wms.model.mongo.warehouse import Warehouse
from wms.server import ConfigParser, IUWMSBackendService

CONFIG_FILE = '/etc/server.yml'


def _setup():
    options = ConfigParser.parse_config_file(CONFIG_FILE)
    options['rate-limiter']['enable'] = False
    application = IUWMSBackendService(options)
    application.connect()


def create_combine_pool():
    warehouse_id = "SHYW"
    warehouse = Warehouse.by_warehouse_id(warehouse_id)
    job_prefix = datetime.utcnow().strftime("%Y%m%d")
    job_id = SequenceIdGenerator.get_sequence_id(job_prefix)
    job = SortJobAccessor.create(
        job_id, CPSortJob.Type.AllocateCabinetLattice, "SHYW")

    inbound_parcels = CPInboundParcel.find({
        "created_datetime": {
            "$gte": datetime(2019, 4, 18, 0, 0, 0),
            "$lte": datetime(2019, 4, 19, 0, 0, 0)
        }
    })

    if not inbound_parcels:
        raise Exception("inbound_parcels is empty")

    combine_ids = list(set(parcel.combine_id for parcel in inbound_parcels))
    parcel_groups = defaultdict(list)
    for parcel in inbound_parcels:
        parcel_groups[parcel.combine_id].append(parcel)

    group_ids = CPSortAllocateGroupId.allocate(len(combine_ids), warehouse.sort_batch_size)
    group_dict = dict(zip(combine_ids, group_ids))

    lattice_id = 1
    cabinet_id = str(ObjectId())
    for combine_id, parcels in parcel_groups.items():
        group_length = len(parcels)
        sort_type = CPSortPool.SortType.DirectShip if group_length == 1 else CPSortPool.SortType.Combined
        for parcel in parcels:
            group_id = group_dict[combine_id]
            CPSortPool.create(
                job_id=job_id,
                tracking_id=parcel.tracking_id,
                sort_type=sort_type,
                group_ids=group_id,
                cabinet_id=cabinet_id,
                lattice_id=lattice_id
            )
        lattice_id += 1


if __name__ == "__main__":
    _setup()
    create_combine_pool()
