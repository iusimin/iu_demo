"""IU Backend API Service

Usage:
    server.py [options]

Options:
    -h --help                   Show this screen.
"""
import cl.backend.server as s
import cl.utils.password as p
import logging
logging.basicConfig(level=logging.DEBUG)
from docopt import docopt
from demo.core.url_mapping import API_ROUTER
import os
from cl.backend.tasks import get_all_tasks
from demo.middlewares.session import SessionMiddleware
from cl.backend.middlewares.validation import RequestValidationMiddleware, RequireJSONMiddleware
import cl.utils.unit_convertor as uc
import demo.tasks as t

CUR_DIR = os.path.abspath(os.path.dirname(__file__))
CONFIG_FILE = '/etc/server.yml'

class IUBackendService(s.BaseBackendService):
    proj_name = 'demo'

    def __init__(self, options):
        async_tasks = get_all_tasks(t)
        super(IUBackendService, self).__init__(
            options,
            API_ROUTER,
            middlewares = [
                RequireJSONMiddleware(),
                RequestValidationMiddleware(),
                SessionMiddleware(),
            ],
            async_tasks = async_tasks,
        )

class ConfigParser(s.ConfigParser):
    @classmethod
    def convert_mapping(cls):
        return {
            'max-memory-per-child': uc.memory_to_kb,
            'login_expire': uc.time_to_second,
            'guest_expire': uc.time_to_second,
            'user_expire': uc.time_to_second,
        }

def main():
    options = ConfigParser.parse_config_file(CONFIG_FILE)
    # Disable rate limiter for web server
    options['rate-limiter']['enable'] = False
    application = IUBackendService(
        options,
    )
    gunicorn_app = s.GunicornApp(application, options['gunicorn'])
    application.logger.info('Server starting...')
    gunicorn_app.run()

if __name__ == "__main__":
    main()