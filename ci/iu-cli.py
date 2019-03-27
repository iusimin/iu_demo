#!/usr/bin/env python
"""IU Developer CLI Tool

Usage:
    iu-cli run <service-name> --env=<ENV> [--shell=<ARGS>] 
    iu-cli compose <compose-target> --env=<ENV> [--shell=<ARGS>]
    iu-cli rebuild --env=<ENV> 
    iu-cli rm --env=<ENV>

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
    all                         Run all service available
    infra                       Infra components like Nginx/DB...
    server                      Backend and frontend web server
    worker                      Worker for all Queue
    worker-shell                Shell to manage workers
    redis-shell                 Shell to manage redis instance
    heavy-task-worker           Worker for heavy task Queue
    light-task-worker           Worker for light task Queue
"""
import os
import sys
from docopt import docopt
from subprocess import call

IU_HOME = os.environ['IU_HOME']

ENV_ALLOWED = {
    'stage': 'stage.yml'
}

SERVICE_CONFIG = {
    'all': [
        'up',
        '--no-recreate', '--abort-on-container-exit',
    ],
    'server': [
        'run',
        '--use-aliases', '--service-ports', '--rm',
        'web-backend',
    ],
    'worker': [
        'run',
        '--use-aliases', '--service-ports', '--rm',
        'web-backend-worker', 'python', 'worker.py', # Need input
    ],
    'worker-shell': [
        'run',
        '--use-aliases', '--service-ports', '--rm',
        'web-backend-worker', '/bin/bash',
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
}

class CommandExecuteFactory(object):
    def __init__(self, env_file):
        self.env_file = env_file
    
    def run_docker_compose(self, args):
        origin_args = ['docker-compose', '-f', os.path.join(
            IU_HOME,
            'ci/docker-compose/%s' % self.env_file
        )]
        call(origin_args + args)
    
    def run_command(self, args):
        call(args)
    
    # def attach_docker_container(self, target):
    #     if target not in ATTACH_CONFIG:
    #         print('ERROR: Invalid attach target %s' % target)
    #         print(__doc__)
    #         sys.exit(1)
    #     self.run_docker_compose(ATTACH_CONFIG[target])

    def run_service(self, service_name, service_args):
        if service_name not in SERVICE_CONFIG:
            print('ERROR: Invalid service %s' % service_name)
            print(__doc__)
            sys.exit(1)
        
        self.run_docker_compose(SERVICE_CONFIG[service_name] + service_args)

def main():
    options = docopt(__doc__)
    env = options.pop('--env')
    if env not in ENV_ALLOWED:
        exit('Invalid --env vaule')
    env_file = ENV_ALLOWED[env]
    cef = CommandExecuteFactory(env_file)
    if not IU_HOME:
        print('ERROR: $IU_HOME variable not set!')
        sys.exit(1)
    if options.pop('rebuild'):
        cef.run_docker_compose(['build'])
    elif options.pop('run'):
        args = options.pop('--shell')
        args = args.split() if args else []
        cef.run_service(
            options.pop('<service-name>'),
            args
        )
    elif options.pop('rm'):
        cef.run_docker_compose(['rm'])
    # elif options.pop('attach'):
    #     cef.attach_docker_container(options.pop('<attach-target>'))
    elif options.pop('compose'):
        args = options.pop('--shell').split()
        cef.run_docker_compose([
            options.pop('<compose-target>'),
            args,
        ])

if __name__ == "__main__":
    main()