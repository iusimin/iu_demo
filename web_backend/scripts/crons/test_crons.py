"""This is a test script

Usage:
    worker.py from-config [--config=<config-string>] <config-name>
    worker.py from-queues [--config=<config-string>] <queue-name>...

Options:
    -c CFG --config CFG         Override configs, format "cfg1=val1,cfg2=val2"
    -h --help                   Show this screen.
"""

from web_backend.server import IUBackendService
from web_backend.server import parse_config_file
from web_backend.server import CONFIG_FILE as SERVER_CONFIG_FILE
from celery.bin import worker
from celery import bootsteps
from docopt import docopt
from web_backend.tasks import AbstractAsyncTaskFactory
import inflection
from kombu import Exchange, Queue

def main():
    args = docopt(__doc__)
    cmd_cfg_string = args.get('--config')

    application = IUBackendService(app_options)
    application.connect()

if __name__ == "__main__":
    main()