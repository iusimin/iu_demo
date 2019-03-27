"""IU Backend Worker Service

Usage:
    worker.py from-config [--config=<config-string>] <config-name>
    worker.py from-queues [--config=<config-string>] <queue-name>...

Options:
    -c CFG --config CFG         Override configs, format "cfg1=val1,cfg2=val2"
    -h --help                   Show this screen.
"""

from web_backend.server import IUBackendService
from web_backend.server import ConfigParser
from web_backend.server import CONFIG_FILE as SERVER_CONFIG_FILE
from celery.bin import worker
from celery import bootsteps
from docopt import docopt
from web_backend.tasks import AbstractAsyncTaskFactory
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

def main():
    args = docopt(__doc__)
    cmd_cfg_string = args.get('--config')
    
    app_options = ConfigParser.parse_config_file(SERVER_CONFIG_FILE)
    worker_options = ConfigParser.parse_config_file(WORKER_CONFIG_FILE)
    application = IUBackendService(app_options)
    application.connect()
    worker_cfg = dict(worker_options['DEFAULT'])
    print(worker_cfg)

    # Override default if from-config
    if args.get('from-config'):
        cfg_name = args.get('<config-name>')
        # Adding prefix for queues
        queue_prefix = AbstractAsyncTaskFactory.queue_prefix()
        if 'queues' in worker_options[cfg_name]:
            queues = ['{queue_prefix}.{queue_name}'.format(
                queue_prefix=queue_prefix,
                queue_name=inflection.underscore(queue_name)
            ) for queue_name in worker_options[cfg_name]['queues']]
            worker_options[cfg_name]['queues'] = ','.join(queues)
        worker_cfg.update(worker_options[cfg_name])
    # Override queues if from-queues
    elif args.get('from-queues'):
        queues = args.get('<queue-name>')
        worker_options[cfg_name]['queues'] = ','.join(queues)
    # Override others from cmd input
    if cmd_cfg_string:
        cmd_cfg = [r.split('=') for r in cmd_cfg_string.split(',')]
        cmd_cfg = {pair[0].strip(): pair[1].strip() for pair in cmd_cfg}
        worker_cfg.update(cmd_cfg)
    # Declare error queues
    iu_worker = worker.worker(app=application.celery_app)
    DeclareDLXnDLQ.init(application.celery_app, worker_cfg['queues'].split(','))
    application.celery_app.steps['worker'].add(DeclareDLXnDLQ)

    iu_worker.run(**worker_cfg)

if __name__ == "__main__":
    main()