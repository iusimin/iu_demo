"""Flower: Celery monitoring and management app

Usage:
    celery-flower.py [options]

Options:
    -h --help                   Show this screen.
"""
from web_backend.server import IUBackendService
from web_backend.server import ConfigParser
from web_backend.server import CONFIG_FILE as SERVER_CONFIG_FILE
from docopt import docopt
from flower.command import FlowerCommand
import flower.options as options

FLOWER_CONFIG_FILE = '/etc/celery-flower.conf'

def main():
    args = docopt(__doc__)
    app_options = ConfigParser.parse_config_file(SERVER_CONFIG_FILE)
    application = IUBackendService(app_options)
    application.connect()
    options.port = 8888
    try:
        flower = FlowerCommand(app=application.celery_app)
        flower.app = application.celery_app
        flower.execute_from_commandline()
    except:
        import sys
        print(bugreport(app=flower.app), file=sys.stderr)
        raise

if __name__ == "__main__":
    main()