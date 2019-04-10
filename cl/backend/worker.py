from celery.bin import worker
from celery import bootsteps
from docopt import docopt
from cl.backend.tasks import AbstractAsyncTaskFactory
import inflection
from kombu import Exchange, Queue

WORKER_CONFIG_FILE = '/etc/worker.yml'

class DeclareDLXnDLQ(bootsteps.StartStopStep):
    requires = {'celery.worker.components:Pool'}

    @classmethod
    def init(cls, celery_app, queues):
        cls.celery_app=celery_app
        cls.queues=queues

    def start(self, worker):
        app = worker.app
        capp = self.celery_app

        dl_exchange_name = capp.conf.deadletter_prefix + capp.conf.default_exchange
        dlx = Exchange(dl_exchange_name,
                       type=capp.conf.default_exchange_type)
        with worker.app.pool.acquire() as conn:
            for q in self.queues:
                dl_queue = Queue(
                    capp.conf.deadletter_prefix+q,
                    exchange=dlx,
                    routing_key=capp.conf.deadletter_prefix+q
                )
                dl_queue.bind(conn).declare()

class AsyncTaskWorker(object):
    def __init__(self, options, application):
        self.application = application
        self.queue_prefix = AbstractAsyncTaskFactory.queue_prefix()
        self.async_tasks_names = [t.__name__ for t in application.async_tasks]
        self.options = options
    
    def run(self, worker_cfg):
        iu_worker = worker.worker(app=self.application.celery_app)
        DeclareDLXnDLQ.init(self.application.celery_app, worker_cfg['queues'].split(','))
        self.application.celery_app.steps['worker'].add(DeclareDLXnDLQ)

        iu_worker.run(**worker_cfg)

    def from_config(self, cfg_name, cmd_cfg={}):
        worker_cfg = dict(self.options['DEFAULT'])
        # Adding prefix for queues
        if 'queues' in self.options[cfg_name]:
            for q in self.options[cfg_name]['queues']:
                if q not in self.async_tasks_names:
                    exit('%s is not a validate task!' % q)
            queues = ['{queue_prefix}.{queue_name}'.format(
                queue_prefix=self.queue_prefix,
                queue_name=inflection.underscore(queue_name)
            ) for queue_name in self.options[cfg_name]['queues']]
            self.options[cfg_name]['queues'] = ','.join(queues)
        worker_cfg.update(self.options[cfg_name])
        worker_cfg.update(cmd_cfg)
        return worker_cfg
    
    def from_queue(self, queues, cmd_cfg={}, process_errors=False):
        worker_cfg = dict(self.options['DEFAULT'])
        for q in queues:
            if q not in self.async_tasks_names:
                exit('%s is not a validate task!' % q)
        error_prefix=self.application.options['celery']['deadletter_prefix']
        if process_errors:
            queue_prefix = error_prefix+self.queue_prefix
        else:
            queue_prefix = self.queue_prefix
        queues = ['{queue_prefix}.{queue_name}'.format(
            queue_prefix=queue_prefix,
            queue_name=inflection.underscore(queue_name)
        ) for queue_name in queues]
        worker_cfg.update({
            'queues': ','.join(queues)
        })
        worker_cfg.update(cmd_cfg)
        return worker_cfg