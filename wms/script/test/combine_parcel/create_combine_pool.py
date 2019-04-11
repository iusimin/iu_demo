# -*- coding: UTF-8 -*-

import logging
import math
import random
from datetime import datetime, timedelta
from itertools import groupby

from bson import ObjectId
from tornado.options import options
from wishwms.core.options import define_for_server
from wishwms.lib.combine_parcel.data_accessor.inbound_parcel_accessor import \
    CPInboundParcelAccessor
from wishwms.lib.combine_parcel.data_accessor.sort_job_accessor import \
    SortJobAccessor
from wishwms.lib.combine_parcel.utilities.inbound_parcel_util import \
    InboundParcelUtil
from wishwms.model.combine_parcel.combine_pool import CPSortGroupId, CPSortPool
from wishwms.model.combine_parcel.inbound_parcel import CPInboundParcel
from wishwms.model.combine_parcel.sort_job import CPSortJob
from wishwms.model.sequence_id_generator import SequenceIdGenerator
from wishwms.server import WishWmsApplication, configure

LOGGER = logging.getLogger("wishwms.test")

def _setup():
    define_for_server()
    configure()
    application = WishWmsApplication(options, LOGGER)
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
