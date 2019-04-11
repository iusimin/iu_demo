"""IU Backend Worker Service

Usage:
    worker.py from-config [--config=<config-string>] <config-name>
    worker.py from-queues [--config=<config-string>] [--process_errors] <queue-name>...

Options:
    -c CFG --config CFG         Override configs, format "cfg1=val1,cfg2=val2"
    --process_errors            Process error queues
    -h --help                   Show this screen.
"""

from demo.server import IUBackendService
from demo.server import ConfigParser
from demo.server import CONFIG_FILE as SERVER_CONFIG_FILE
from docopt import docopt
from cl.backend.worker import AsyncTaskWorker

WORKER_CONFIG_FILE = '/etc/worker.yml'

def main():
    args = docopt(__doc__)
    cmd_cfg_string = args.get('--config')
    if cmd_cfg_string:
        cmd_cfg = [r.split('=') for r in cmd_cfg_string.split(',')]
        cmd_cfg = {pair[0].strip(): pair[1].strip() for pair in cmd_cfg}
    else:
        cmd_cfg = {}

    app_options = ConfigParser.parse_config_file(SERVER_CONFIG_FILE)
    worker_options = ConfigParser.parse_config_file(WORKER_CONFIG_FILE)
    app_options['env']['instance'] = 'worker'
    if args.get('--process_errors'):
        app_options['celery']['process_errors'] = True
    application = IUBackendService(app_options)
    application.connect()
    worker = AsyncTaskWorker(worker_options, application)
    
    if args.get('from-config'):
        cfg_name = args.get('<config-name>')
        worker_cfg = worker.from_config(cfg_name, cmd_cfg)
    elif args.get('from-queues'):
        queues = args.get('<queue-name>')
        process_errors = args.get('--process_errors', False)
        worker_cfg = worker.from_queue(queues, cmd_cfg, process_errors)
    worker.run(worker_cfg)

if __name__ == "__main__":
    main()