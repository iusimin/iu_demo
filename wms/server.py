"""IU WMS Backend API Service

Usage:
    server.py [options]

Options:
    -h --help                   Show this screen.
"""
import logging
import os
import subprocess

from docopt import docopt

import cl.backend.server as s
import cl.utils.password as p
import cl.utils.unit_convertor as uc
import wms.tasks as t
from cl.backend.middlewares.validation import (RequestValidationMiddleware,
                                               RequireJSONMiddleware)
from cl.backend.tasks import get_all_tasks
from wms.core.url_mapping import API_ROUTER, STATIC_ROUTE
from wms.middlewares.session import SessionMiddleware

logging.basicConfig(level=logging.DEBUG)

CUR_DIR = os.path.abspath(os.path.dirname(__file__))
CONFIG_FILE = '/etc/server.yml'

class IUWMSBackendService(s.BaseBackendService):
    proj_name = 'wms'

    def __init__(self, options):
        async_tasks = get_all_tasks(t)
        super(IUWMSBackendService, self).__init__(
            options,
            API_ROUTER,
            middlewares = [
                RequireJSONMiddleware(),
                RequestValidationMiddleware(),
                SessionMiddleware(),
            ],
            async_tasks = async_tasks,
        )

        # Build static route
        for (uri, path) in STATIC_ROUTE:
            abs_path = os.path.join(CUR_DIR, path)
            self.add_static_route(uri, abs_path)

    def build_web_resource(self):
        cwd = os.path.join(CUR_DIR, "web")
        command = "npm install && npm run build"
        return subprocess.Popen(command, cwd=cwd, shell=True, stderr=subprocess.STDOUT)

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
    application = IUWMSBackendService(
        options
    )

    #build_web_process = self.application.build_web_resource()
    #build_web_ret = build_web_process.wait()
    #if build_web_ret != 0:
    #   raise subprocess.CalledProcessError(build_web_ret, "npm")

    gunicorn_app = s.GunicornApp(application, options['gunicorn'])
    application.logger.info('Server starting...')
    gunicorn_app.run()

if __name__ == "__main__":
    main()
