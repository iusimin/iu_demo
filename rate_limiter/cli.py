#!/usr/bin/env python
"""Rate Limiter CLI Tool

Usage:
    cli.py manage
    cli.py list
"""
import os
import sys
from docopt import docopt
from subprocess import call
import uuid
from shutil import copyfile, rmtree
from nginxparser import loads
import re
import yaml
from contextlib import contextmanager

QUEUE_RATE_FILE = '/etc/rate_limiter/queue_rate.conf'
ZONES_FILE = '/etc/rate_limiter/zones.conf'

ZONE_PATTERN = 'zone=([^:]+):50m\s+rate=(.+)'
QUEUE_ZONE_PATTERN = 'zone=([^\s]+)'
BURST_PATTERN = 'burst=(\d+)'
DELAY_PATTERN = 'delay=(\d+)'

ZONES_TEMPLATE = '''
limit_req_zone $request_uri zone=%(zone_name)s:50m          rate=%(rate)s;
'''
QUEUE_RATE_TEMPLATE = '''
location ~ \.%(queue_name)s$ {
    limit_req zone=%(zone_name)s %(burst)s %(nodelay)s %(delay)s;
    alias /etc/rate_limiter/static/index.html;
}
'''
DOC = '''# Rate limiter config
# Example:
# queue-name:
#   rate: 10r/s (required)
#   burst: 10 (optional)
#   delay: 10 (optional)
#   nodelay: True (optional)
# See nginx doc to understand each options:
#   https://www.nginx.com/blog/rate-limiting-nginx/
'''

def parse_nginx_config():
    queue_rates = open(QUEUE_RATE_FILE).read()
    zones = open(ZONES_FILE).read()
    if len(queue_rates) == 0 or len(zones) == 0:
        return ''
    queue_rates = loads(queue_rates)
    zones = loads(zones)
    configs = {}
    zone_map = {}
    for z in zones:
        zstr = z[1]
        regex = re.search(ZONE_PATTERN, zstr)
        if regex:
            zone_map[regex.group(1)] = regex.group(2)
    for r in queue_rates:
        queue_name = r[0][-1]
        queue_name = re.search('\w+', queue_name).group(0)
        qoptions = r[1][0][-1]
        zone = re.search(QUEUE_ZONE_PATTERN, qoptions)
        burst = re.search(BURST_PATTERN, qoptions)
        nodelay = 'nodelay' in qoptions
        delay = re.search(DELAY_PATTERN, qoptions)
        zone_rate = zone_map.get(zone.group(1))
        if zone_rate is None:
            exit('Invalid zone define %s' % zone)
        configs[queue_name] = {
            'rate': zone_rate
        }
        if burst:
            configs[queue_name]['burst'] = int(burst.group(1))
        if nodelay:
            configs[queue_name]['nodelay'] = True
        if delay:
            configs[queue_name]['delay'] = int(delay.group(1))
    return yaml.dump(configs)

@contextmanager
def parse_config_file(readonly=False):
    tmp_file_path = '/tmp/%s.yml' % uuid.uuid4().hex
    queue_rate_bak_path = '/tmp/queue_rate.%s.conf' % uuid.uuid4().hex
    zones_bak_path = '/tmp/zones.%s.conf' % uuid.uuid4().hex
    tmp_file_content = '%s\n%s' % (DOC, parse_nginx_config())
    try:
        f = open(tmp_file_path, 'w')
        f.write(tmp_file_content)
        f.close()
        yield tmp_file_path # Give control to user for editing
        if readonly:
            return
        new_file_content = open(tmp_file_path).read()
        if new_file_content == tmp_file_content:
            print('No modification...')
            return
        new_config = yaml.safe_load(new_file_content)
        if not new_config:
            print('Empty config file...')
            return
        if not isinstance(new_config, dict):
            raise Exception('Bad configuration format')
        # Backup old config
        if os.path.exists(QUEUE_RATE_FILE):
            copyfile(QUEUE_RATE_FILE, queue_rate_bak_path)
        if os.path.exists(ZONES_FILE):
            copyfile(ZONES_FILE, zones_bak_path)
        # Generate new config
        zrows = []
        qrows = []
        for qname, cfg in new_config.items():
            rate = cfg.get('rate')
            if rate is None:
                raise Exception('Rate is not set for queue %s' % qname)
            zone_name = 'z%s' % rate.replace('/', '')
            burst = 'burst=%s'%cfg['burst'] if 'burst' in cfg else ''
            nodelay = 'nodelay' if 'nodelay' in cfg else ''
            delay = 'delay=%s'%cfg['delay'] if 'delay' in cfg else ''
            zrows.append(ZONES_TEMPLATE % {
                'zone_name': zone_name,
                'rate': cfg.get('rate'),
            })
            qrows.append(QUEUE_RATE_TEMPLATE % {
                'queue_name': qname,
                'zone_name': zone_name,
                'burst': burst,
                'delay': delay,
                'nodelay': nodelay,
            })
        # Writing templates
        f = open(QUEUE_RATE_FILE, 'w')
        f.write('\n'.join(qrows))
        f.close()
        f = open(ZONES_FILE, 'w')
        f.write('\n'.join(zrows))
        f.close()
        ret = call(['service', 'nginx', 'reload'])
        if ret > 0:
            raise Exception('Bad configuration')
    except Exception:
        print('Rollback changes...')
        if os.path.exists(queue_rate_bak_path):
            copyfile(queue_rate_bak_path, QUEUE_RATE_FILE)
        if os.path.exists(zones_bak_path):
            copyfile(zones_bak_path, ZONES_FILE)
        raise
    finally:
        print('Clear tmp file...')
        if os.path.exists(tmp_file_path):
            os.remove(tmp_file_path)
        if os.path.exists(queue_rate_bak_path):
            os.remove(queue_rate_bak_path)
        if os.path.exists(zones_bak_path):
            os.remove(zones_bak_path)

def main():
    options = docopt(__doc__)
    readonly = False
    if options.pop('list'):
        readonly=True
    elif options.pop('manage'):
        readonly=False
    with parse_config_file(readonly=readonly) as tmp_cfg_path:
        if readonly:
            ret = call(['vim', '+', '-R', tmp_cfg_path])
        else:
            ret = call(['vim', '+', tmp_cfg_path])
        if ret > 0:
            raise Exception('Editor raise error, aborting...')

if __name__ == "__main__":
    main()