#!/usr/bin/env python
"""IU Developer CLI Tool

Usage:
    iu-cli <proj> run <service-name> --env=<ENV> [--shell=<ARGS>] 
    iu-cli <proj> compose <compose-command> <compose-target> --env=<ENV> [--shell=<ARGS>]
    iu-cli <proj> rebuild --env=<ENV> [<rebuild-targets>...]
    iu-cli <proj> rm --env=<ENV> [<remove-targets>...]

Projects:
    demo                        IU Demo Project
    wms                         WMS Project

Options:
    -e ENV --env ENV            Running environment
    -s ARGS --shell ARGS        Pass shell arguments to starting service
    -h --help                   Show this screen.

Sub Commands:
    run                         Run pre-defined service.
    compose                     Run origin docker-compose service
    rebuild                     Rebuild all images
    rm                          Clear stopped containers
    attach                      Attach to a running service

Pre-defined Services:
    infra                       Infra components like Nginx/DB...
    server                      Backend and frontend web server
    wms                 WMS server
    worker                      Worker for all Queue
    worker-shell                Shell to manage workers
    redis-shell                 Shell to manage redis instance
    heavy-task-worker           Worker for heavy task Queue
    light-task-worker           Worker for light task Queue
    rate-limiter-config         Open and edit rate limiter config
"""
import os
import sys
from docopt import docopt
from subprocess import call

IU_HOME = os.environ['IU_HOME']
CFG_FILE = os.path.join(IU_HOME, '.iu_cli')

ENV_ALLOWED = {
    'stage': 'stage.yml'
}

SERVICE_CONFIG = {
    'demo': {
        'server': [
            'run',
            '--use-aliases', '--service-ports', '--rm',
            'demo',
        ],
        'worker': [
            'run',
            '--use-aliases', '--service-ports', '--rm',
            'demo-worker', 'python', 'worker.py', # Need input
        ],
        'worker-shell': [
            'run',
            '--use-aliases', '--service-ports', '--rm',
            'demo-worker', '/bin/bash',
        ],
        'redis-shell': [
            'run',
            '--use-aliases', '--service-ports', '--rm',
            'redis', '/bin/bash',
        ],
        'infra': [
            'up',
            '--abort-on-container-exit',
            'nginx', 'mongodb', 'mongo-express', 'rabbitmq', 'celery-flower', 'rate-limiter', 'redis'
        ],
        'rate-limiter-config': [
            'exec', 'rate-limiter',
            'python3', 'cli.py', 'manage',
        ],
    },
    'wms': {
        'vue-frontend-server': [
            'run',
            '--use-aliases', '--service-ports', '--rm',
            'vue-frontend',
        ],
        'server': [
            'run',
            '--use-aliases', '--service-ports', '--rm',
            'wms',
        ],
        'infra': [
            'up',
            '--abort-on-container-exit',
            'nginx', 'mongodb', 'mongo-express', 'rabbitmq', 'celery-flower', 'rate-limiter', 'redis'
        ]
    }
}

class CommandExecuteFactory(object):
    def __init__(self, proj, env_file):
        self.proj = proj
        self.env_file = env_file
        self.service_cfg = SERVICE_CONFIG[self.proj]
    
    def run_docker_compose(self, args):
        origin_args = ['docker-compose', '-f', os.path.join(
            IU_HOME,
            'ci/docker-compose/%s/%s' % (self.proj, self.env_file)
        )]
        call(origin_args + args)
    
    def run_command(self, args):
        call(args)

    def run_service(self, service_name, service_args):
        if service_name not in self.service_cfg:
            print(self.service_cfg)
            print('ERROR: Invalid service %s' % service_name)
            print(__doc__)
            sys.exit(1)
        
        self.run_docker_compose(self.service_cfg[service_name] + service_args)

def main():
    options = docopt(__doc__)
    proj = options.pop('<proj>')
    env = options.pop('--env')
    if env not in ENV_ALLOWED:
        exit('Invalid --env vaule')
    env_file = ENV_ALLOWED[env]
    cef = CommandExecuteFactory(proj, env_file)
    if not IU_HOME:
        print('ERROR: $IU_HOME variable not set!')
        sys.exit(1)
    if options.pop('rebuild'):
        targets = options.pop('<rebuild-targets>')
        cef.run_docker_compose(['rm']+targets)
        cef.run_docker_compose(['build']+targets)
    elif options.pop('run'):
        args = options.pop('--shell')
        args = args.split() if args else []
        cef.run_service(
            options.pop('<service-name>'),
            args
        )
    elif options.pop('rm'):
        targets = options.pop('<remove-targets>')
        cef.run_docker_compose(['rm']+targets)
    elif options.pop('compose'):
        args = [
            options.pop('<compose-command>'),
            options.pop('<compose-target>'),
        ]
        args = args + options.pop('--shell').split()
        cef.run_docker_compose(args)

if __name__ == "__main__":
    main()