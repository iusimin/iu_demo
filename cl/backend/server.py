from gevent import monkey
monkey.patch_all()
import falcon
from gunicorn.app.base import BaseApplication

import yaml
import mongoengine
from celery import Celery
from cl.backend.tasks import AbstractAsyncTaskFactory
from cl.backend.api import convert_custom_verb_pattern
from kombu import Exchange, Queue
import walrus
from cl.utils.redis import BaseRedisKey
import redis

class BaseBackendService(falcon.API):
    options = {}
    
    @property
    def proj_name(self):
        raise NotImplementedError()
    
    @property
    def logger(self):
        return logging.getLogger('iu.{proj_name}'.format(
            proj_name = self.proj_name,
        ))

    def __init__(self, options, url_router, middlewares=[], async_tasks=[]):
        self.options = options
        self.logger.setLevel(logging.INFO)
        self.url_router = url_router
        self.async_tasks = async_tasks
        super(BaseBackendService, self).__init__(middleware=middlewares)

        falcon_options = options.pop('falcon', {})
        if 'req_options' in falcon_options:
            for k, v in falcon_options.pop('req_options').items():
                setattr(self.req_options, k, v)
        if 'resp_options' in falcon_options:
            for k, v in falcon_options.pop('resp_options').items():
                setattr(self.resp_options, k, v)
        
        # Build routers
        for (uri, resource) in url_router:
            self.add_route(uri, resource(self))
        # Adding custom verb router
        for (uri, resource) in url_router:
            if not resource.ENABLE_CUSTOM_VERB:
                continue
            uri = convert_custom_verb_pattern(uri)
            self.add_route(uri, resource(self, custom_verb=True))

    def connect(self):
        self.connect_mongo()
        self.connect_redis()
        self.connect_celery()
    
    def connect_mongo(self):
        for opts in self.options['mongo']:
            self.mongo_connections = mongoengine.connect(
                **opts)
            self.logger.info('Connecting mongo %(alias)s: %(host)s:%(port)s/%(db)s' \
                % opts)

    def connect_redis(self):
        self.redis_db = walrus.Database(**self.options['redis'])
        self.redis_conn = redis.Redis(**self.options['redis'])
        BaseRedisKey.init(self)
        self.logger.info('Connecting mongo: %(host)s:%(port)s/%(db)s' \
            % self.options['redis'])

    def connect_celery(self):
        self.logger.info('Connecting Celery...')
        self.celery_app = Celery(self.proj_name)
        self.celery_app.conf.update(**self.options['celery'])
        cfg = self.celery_app.conf
        # Setup tasks
        AbstractAsyncTaskFactory.init(self)
        for t in self.async_tasks:
            t.init(self)
        # Setup exchange, DLQ will be setup in worker.py
        default_exchange = Exchange(cfg.default_exchange,
            type=cfg.default_exchange_type)
        # Setup router for each task
        task_routes = {}
        task_queues = []
        for t in self.async_tasks:
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
        return {}

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