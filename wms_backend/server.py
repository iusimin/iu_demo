"""IU WMS Backend API Service

Usage:
    server.py [options]

Options:
    -h --help                   Show this screen.
"""
import logging
import os

import yaml
from docopt import docopt

import cl.utils.password as p
import falcon
import redis
import walrus
import wms_backend.lib.cache as cache
import wms_backend.lib.unit_convertor as uc
import wms_backend.tasks.all as async_tasks
from celery import Celery
from cl.utils.redis import BaseRedisKey
from gevent import monkey
from gunicorn.app.base import BaseApplication
from iu_mongo import connect as mongo_connect
from kombu import Exchange, Queue
from wms_backend.api import convert_custom_verb_pattern
from wms_backend.core.url_mapping import API_ROUTER
from wms_backend.middlewares.session import SessionMiddleware
from wms_backend.middlewares.validation import (RequestValidationMiddleware,
                                                RequireJSONMiddleware)
from wms_backend.tasks import AbstractAsyncTaskFactory

monkey.patch_all()
logging.basicConfig(level=logging.DEBUG)


CUR_DIR = os.path.abspath(os.path.dirname(__file__))
CONFIG_FILE = '/etc/server.yml'
PROJ_NAME = 'wms_backend'

class IUWMSBackendService(falcon.API):
    options = {}

    def __init__(self, options):
        self.options = options
        self.logger = logging.getLogger('iu.wms_backend')
        self.logger.setLevel(logging.INFO)
        super(IUWMSBackendService, self).__init__(middleware=[
            RequireJSONMiddleware(),
            RequestValidationMiddleware(),
            SessionMiddleware(),
        ])

        falcon_options = options.pop('falcon', {})
        if 'req_options' in falcon_options:
            for k, v in falcon_options.pop('req_options').items():
                setattr(self.req_options, k, v)
        if 'resp_options' in falcon_options:
            for k, v in falcon_options.pop('resp_options').items():
                setattr(self.resp_options, k, v)
        
        # Build routers
        for (uri, resource) in API_ROUTER:
            self.add_route(uri, resource(self))
        # Adding custom verb router
        for (uri, resource) in API_ROUTER:
            if not resource.ENABLE_CUSTOM_VERB:
                continue
            uri = convert_custom_verb_pattern(uri)
            self.add_route(uri, resource(self, custom_verb=True))

    def connect(self):
        self.connect_mongo()
        self.connect_redis()
        self.connect_celery()
    
    def connect_mongo(self):
        self.mongo_connections = mongo_connect(
            **self.options['mongo'])
        self.logger.info('Connecting mongo: %(host)s:%(port)s/%(db_names)s' \
            % self.options['mongo'])

    def connect_redis(self):
        self.redis_db = walrus.Database(**self.options['redis'])
        self.redis_conn = redis.Redis(**self.options['redis'])
        BaseRedisKey.init(self)
        self.logger.info('Connecting mongo: %(host)s:%(port)s/%(db)s' \
            % self.options['redis'])

    def connect_celery(self):
        self.logger.info('Connecting Celery...')
        self.celery_app = Celery(PROJ_NAME)
        self.celery_app.conf.update(**self.options['celery'])
        cfg = self.celery_app.conf
        # Setup tasks
        AbstractAsyncTaskFactory.init(self)
        for t in async_tasks.ALL:
            t.init(self)
        # Setup exchange, DLQ will be setup in worker.py
        default_exchange = Exchange(cfg.default_exchange,
            type=cfg.default_exchange_type)
        # Setup router for each task
        task_routes = {}
        task_queues = []
        for t in async_tasks.ALL:
            task_routes.update(t.ROUTES)
            task_queues.append(Queue(
                t.queue_name(),
                exchange=default_exchange,
                routing_key=t.queue_name(),
            ))
        self.celery_app.conf.task_queues = task_queues
        self.celery_app.conf.task_routes = task_routes

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
        self.application.logger.info('Server is now running...')
        return self.application

class ConfigParser(object):
    @classmethod
    def convert_mapping(cls):
        return {
            'max-memory-per-child': uc.memory_to_kb,
            'login_expire': uc.time_to_second,
            'guest_expire': uc.time_to_second,
            'user_expire': uc.time_to_second,
        }

    @classmethod
    def parse_config_file(cls, fpath):
        f = open(fpath, 'r')
        raw = yaml.full_load(f)
        convert_mapping = cls.convert_mapping()
        def __convert_unit(d):
            for k, v in d.items():
                if isinstance(v, dict):
                    __convert_unit(v)
                elif k in convert_mapping:
                    d[k] = convert_mapping[k](v)
        __convert_unit(raw)
        return raw

def main():
    options = ConfigParser.parse_config_file(CONFIG_FILE)
    # Disable rate limiter for web server
    options['rate-limiter']['enable'] = False
    application = IUWMSBackendService(options)
    gunicorn_app = GunicornApp(application, options['gunicorn'])
    application.logger.info('Server starting...')
    gunicorn_app.run()

if __name__ == "__main__":
    main()
