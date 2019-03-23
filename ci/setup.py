#!/usr/bin/env python
import os
from contextlib import contextmanager

IU_HOST_START = '# BEGIN - IU hosts setup\n'
IU_HOST_END = '# END - IU hosts setup\n'
TMP_HOSTS = '/tmp/iu-setup-hosts'
BACKUP_HOSTS = '/tmp/hosts.iu.BAK'

@contextmanager
def print_step(txt):
    print('*** '+txt+'...')
    yield
    print('*** '+txt+'... Done')

def main():
    if 'IU_HOME' not in os.environ:
        exit('Please setup $IU_HOME environment variable!')
    with print_step('Installing iu-cli'):
        os.system('sudo pip install docopt')
        os.system('sudo ln -s $IU_HOME/ci/iu-cli.py /usr/local/bin/iu-cli')
        os.system('sudo chmod 755 /usr/local/bin/iu-cli')
    with print_step('Build container images'):
        os.system('docker-compose -f $IU_HOME/ci/docker-compose/stage.yml build')
    with print_step('Updating /etc/hosts'):
        origin_rows = open('/etc/hosts', 'r').readlines()
        st = origin_rows.index(IU_HOST_START) if IU_HOST_START in origin_rows else None
        ed = origin_rows.index(IU_HOST_END) if IU_HOST_END in origin_rows else None
        try:
            # Backup old hosts
            os.system('cp /etc/hosts %s' % BACKUP_HOSTS)
            tmp_f = open(TMP_HOSTS, 'w')
            for idx, r in enumerate(origin_rows):
                if st is None or ed is None or idx < st or idx > ed:
                    tmp_f.write(r)
            tmp_f.close()
            os.system('cat $IU_HOME/ci/hosts >> %s' % TMP_HOSTS)
            os.system('sudo sh -c "cp %s /etc/hosts"' % TMP_HOSTS)
        finally:
            if os.path.exists(TMP_HOSTS):
                os.remove(TMP_HOSTS)

if __name__ == '__main__':
    main()