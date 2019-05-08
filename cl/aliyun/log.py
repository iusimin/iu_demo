import logging
import time

import logstash
import random

host = 'localhost'
# logger_name: database.outputs.table_name
# outputs:
# 1. oss: only store data to oss for hive/spark query later(cheap, won't delete)
# 2. es: only store data to es, for real-time monitoring or dashboard
#        (expansive, maybe keep only for 7 days or 14 days)
#        use this for system monitoring usually
# 3. full: both oss and es, should use this for most business cases

es_logger = logging.getLogger('iu_demo.es.es_only_table')
oss_logger = logging.getLogger('iu_demo.oss.oss_only_table')
es_oss_logger = logging.getLogger('iu_demo.full.es_oss_table')

loggers = [es_logger, oss_logger, es_oss_logger]
for test_logger in loggers:
    test_logger.setLevel(logging.DEBUG)
    test_logger.addHandler(logstash.TCPLogstashHandler(host, 5000, version=1))

    test_logger.debug('DEBUG Message')
    test_logger.info('INFO Message')
    test_logger.warning('WARNING Message')
    test_logger.error('ERROR Message')

for i in range(100):
    for test_logger in loggers:
        # add extra field to logstash message
        extra = {
            'test_string': test_logger.name,
            'test_boolean': True,
            'test_dict': {'iter': i, 'b': 'c'},
            'test_float': random.random(),
            'test_integer': random.randint(0, 100),
            'test_list': [1, 2, 3],
        }
        test_logger.info('log_data', extra=extra)
    time.sleep(1)


