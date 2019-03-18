#!/usr/bin/env python
"""IU Developer CLI Tool

Usage:
    iu-cli [options] run <service-name>
    iu-cli [options] rebuild
    iu-cli [options] rm

Options:
    -e ENV --env ENV            Running environment
    -h --help                   Show this screen.

Service Names:
    infra                       Infra components like Nginx/DB...
    server                      Backend and frontend web server
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
    'server': [
        'run',
        '--use-aliases', '--service-ports',
        'web-backend',
    ],
    'infra': [
        'up',
        '--no-recreate', '--abort-on-container-exit',
        'nginx', 'mongodb', 'mongo-express',
    ]
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

    def run_service(self, service_name):
        if service_name not in SERVICE_CONFIG:
            print('ERROR: Invalid service %s' % service_name)
            print(__doc__)
            sys.exit(1)
        
        self.run_docker_compose(SERVICE_CONFIG[service_name])

def main():
    options = docopt(__doc__)
    env = options.pop('--env')
    if not env or env not in ENV_ALLOWED:
        print('ERROR: Invalid --env option')
        sys.exit(1)
    env_file = ENV_ALLOWED[env]
    cef = CommandExecuteFactory(env_file)
    if not IU_HOME:
        print('ERROR: $IU_HOME variable not set!')
        sys.exit(1)
    if options.pop('rebuild'):
        cef.run_docker_compose(['build'])
    elif options.pop('run'):
        cef.run_service(options.pop('<service-name>'))
    elif options.pop('rm'):
        cef.run_docker_compose(['rm'])

if __name__ == "__main__":
    main()