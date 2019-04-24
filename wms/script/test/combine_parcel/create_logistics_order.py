# -*- coding: UTF-8 -*-

from datetime import datetime

from wms.lib.logistics_order.data_accessor.logistics_order_accessor import \
    LogisticsOrderAccessor
from wms.model.mongo.logistics.logistics_order import LogisticsOrder
from wms.model.mongo.warehouse import CPWarehouse
from wms.server import ConfigParser, IUWMSBackendService

CONFIG_FILE = '/etc/server.yml'

def _setup():
    options = ConfigParser.parse_config_file(CONFIG_FILE)
    options['rate-limiter']['enable'] = False
    application = IUWMSBackendService(options)
    application.connect()

def create_warehouse():
    tracking_count = 100
    tracking_prefix = "LO{0}".format(datetime.now().strftime("%Y%m%d%H%M"))

    for i in range(tracking_count):
        tracking_id = tracking_prefix + "{:03d}".format(i)
        LogisticsOrderAccessor.create_order(
            tracking_id=tracking_id,
            platform_id="5cc08855e48ab7003ab15b2a",
            carrier_id="5cc08832e48ab70035d25b22"
        )

if __name__ == "__main__":
    _setup()
    create_warehouse()
