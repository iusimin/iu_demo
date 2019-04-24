# -*- coding: UTF-8 -*-

from datetime import datetime

from wms.model.mongo.logistics.logistics_carrier import LogisticsCarrier
from wms.model.mongo.logistics.logistics_platform import LogisticsPlatform
from wms.server import ConfigParser, IUWMSBackendService

CONFIG_FILE = '/etc/server.yml'


def _setup():
    options = ConfigParser.parse_config_file(CONFIG_FILE)
    options['rate-limiter']['enable'] = False
    application = IUWMSBackendService(options)
    application.connect()


def create_logistics_carrier():
    LogisticsCarrier.create_if_not_exist(u"CHINA POST", u"中国邮政")


def create_logistics_platform():
    LogisticsPlatform.create_if_not_exist(u"Intelligence Union", u"汇聚")


if __name__ == "__main__":
    _setup()
    create_logistics_carrier()
    create_logistics_platform()
