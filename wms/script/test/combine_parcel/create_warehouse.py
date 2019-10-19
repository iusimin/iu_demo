# -*- coding: UTF-8 -*-

from wms.model.mongo.warehouse import Warehouse
from wms.server import ConfigParser, IUWMSBackendService

CONFIG_FILE = '/etc/server.yml'

def _setup():
    options = ConfigParser.parse_config_file(CONFIG_FILE)
    options['rate-limiter']['enable'] = False
    application = IUWMSBackendService(options)
    application.connect()

def create_warehouse():
    Warehouse.create(
        warehouse_id="SHYW",
        warehouse_name="SHANGHAI-YANWEN01",
        cabinet_count=8,
        cabinet_width=8,
        cabinet_height=5,
        sort_batch_size=8
    )


if __name__ == "__main__":
    _setup()
    create_warehouse()
