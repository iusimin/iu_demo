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
from wms.model.mongo.warehouse import CPWarehouse
from wms.server import ConfigParser, IUWMSBackendService

CONFIG_FILE = '/etc/server.yml'


def _setup():
    options = ConfigParser.parse_config_file(CONFIG_FILE)
    options['rate-limiter']['enable'] = False
    application = IUWMSBackendService(options)
    application.connect()

def create_inbound_parcels():
    combine_id_count = 30
    tracking_count = 100

    tracking_prefix = "CP{0}".format(datetime.now().strftime("%Y%m%d%H%M"))
    combine_id_pool = [str(ObjectId()) for i in range(combine_id_count)]
    for i in range(tracking_count):
        combine_id = combine_id_pool[random.randint(0, combine_id_count - 1)]
        tracking_id = tracking_prefix + "{:03d}".format(i)

        InboundParcelUtil.create_parcel(
            tracking_id=tracking_id,
            combine_id=combine_id,
            warehouse_id="CHINAPOST-SH001",
            inbound_carrier=0,
            latest_ship_datetime=datetime.now() + timedelta(days=random.randint(3,5))
        )

def inbound_parcel():
    inbound_parcels = CPInboundParcel.find(
        {
            "created_datetime": {
                "$gte": datetime(2019, 4, 18, 0, 0, 0),
                "$lte": datetime(2019, 4, 19, 0, 0, 0)
            }
        }
    )

    for parcel in inbound_parcels:
        InboundParcelUtil.inbound_parcel(
            tracking_id=parcel.tracking_id,
            parcel_type=CPInboundParcel.ParcelType.Ordinary,
            weight=random.uniform(0.1, 1.2),
            has_battery=False,
            has_liquid=False,
            has_sensitive=False
        )

def set_ready_to_ship():
    inbound_parcels = CPInboundParcel.find(
        {
            "created_datetime": {
                "$gte": datetime(2019, 4, 18, 0, 0, 0),
                "$lte": datetime(2019, 4, 19, 0, 0, 0)
            }
        }
    )

    for parcel in inbound_parcels:
        parcel.set(ready_to_ship=True)

if __name__ == "__main__":
    _setup()
    create_inbound_parcels()
    #inbound_parcel()
    #set_ready_to_ship()
