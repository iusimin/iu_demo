# -*- coding: UTF-8 -*-

import random
from datetime import datetime, timedelta

from bson import ObjectId

from wms.lib.combine_parcel.data_accessor.inbound_parcel_accessor import \
    CPInboundParcelAccessor
from wms.lib.combine_parcel.utilities.inbound_parcel_util import \
    InboundParcelUtil
from wms.model.mongo.combine_parcel.inbound_parcel import \
    CPInboundParcel
from wms.model.mongo.warehouse_info import CPWarehouse
from wms.server import ConfigParser, IUWMSBackendService

CONFIG_FILE = '/etc/server.yml'


def _setup():
    options = ConfigParser.parse_config_file(CONFIG_FILE)
    options['rate-limiter']['enable'] = False
    application = IUWMSBackendService(options)
    application.connect()

def create_combine_pool():
    job_prefix = datetime.utcnow().strftime("%Y%m%d")
    job_id = SequenceIdGenerator.get_sequence_id(job_prefix)
    job = SortJobAccessor.create(job_id, CPSortJob.Type.AllocateCabinetLattice, "CHINAPOST-SH001")

    inbound_parcels = CPInboundParcel.find({
        "created_datetime": {
            "$gte": datetime(2019, 4, 4, 0, 0, 0),
            "$lte": datetime(2019, 4, 5, 0, 0, 0)
        }
    })

    key_func = lambda x: x.combine_id
    inbound_parcels = sorted(inbound_parcels, key=key_func)
    parcel_groups = groupby(inbound_parcels, key=key_func)


    lattice_id = 1
    cabinet_id = str(ObjectId())
    for group in parcel_groups:
        parcels = list(group[1])
        group_length = len(parcels)
        sort_type = CPSortPool.SortType.DirectShip if group_length == 1 else CPSortPool.SortType.Combined
        for parcel in parcels:
            CPSortPool.create(
                job_id=job_id,
                tracking_id=parcel.tracking_id,
                sort_type=sort_type,
                group_ids=[],
                cabinet_id=cabinet_id,
                lattice_id=lattice_id
            )
        lattice_id += 1
    

if __name__ == "__main__":
    _setup()
    create_combine_pool()
