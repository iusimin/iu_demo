# -*- coding: UTF-8 -*-

from wms.model.mongo.warehouse_info import CPWarehouse
from wms.server import ConfigParser, IUWMSBackendService

CONFIG_FILE = '/etc/server.yml'

def _setup():
    options = ConfigParser.parse_config_file(CONFIG_FILE)
    options['rate-limiter']['enable'] = False
    application = IUWMSBackendService(options)
    application.connect()

def create_warehouse():
    CPWarehouse.create(
        warehouse_id="CHINAPOST-SH001",
        warehouse_name="CHINAPOST-DONGGUAN",
        cabinet_count=8,
        cabinet_width=8,
        cabinet_height=5,
        sort_batch_size=8
    )


if __name__ == "__main__":
    _setup()
    create_warehouse()
