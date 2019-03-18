"""IU Backend API Service

Usage:
    server.py [options]

Options:
    -h --help                   Show this screen.
"""
from gevent import monkey
monkey.patch_all()
import falcon
import cl.utils.password as p
import logging
logging.basicConfig(level=logging.DEBUG)
from docopt import docopt
from gunicorn.app.base import BaseApplication

from web_backend.core.url_mapping import API_ROUTER
import yaml
import os
import mongoengine

CUR_DIR = os.path.abspath(os.path.dirname(__file__))
CONFIG_FILE = '/etc/iu-web-backend.yml'

class IUBackendService(falcon.API):
    options = {}

    def __init__(self, options):
        super(IUBackendService, self).__init__(middleware=[
        ])
        self.options = options
        self.logger = logging.getLogger('iu.web_backend')
        self.logger.setLevel(logging.INFO)

        # Build routers
        for (uri, resource) in API_ROUTER:
            self.add_route(uri, resource(self))

    def connect(self):
        self.connect_mongo()
    
    def connect_mongo(self):
        self.mongo_connections = mongoengine.connect(
            **self.options['mongo'])
        self.logger.info('Connecting mongo: %(host)s:%(port)s/%(db)s' \
            % self.options['mongo'])

    def disconnect(self):
        pass

class GunicornApp(BaseApplication):
    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super(GunicornApp, self).__init__()

    def load_config(self):
        for key, value in self.options.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        self.application.connect()
        return self.application

def parse_config_file(fpath):
    f = open(fpath, 'r')
    return yaml.full_load(f)

def main():
    options = parse_config_file(CONFIG_FILE)
    application = IUBackendService(options)
    gunicorn_app = GunicornApp(application, options['gunicorn'])
    application.logger.info('Server starting...')
    gunicorn_app.run()

if __name__ == "__main__":
    main()