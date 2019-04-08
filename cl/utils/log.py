# encoding: utf8
import logging, logging.config, os

# 配置
import random

text_conf = {'version': 1,
        'formatters': {'rawformatter': {'class': 'logging.Formatter',
                                        'format': '%(message)s'}
                       },
        'handlers': {'sls_handler': {'()':
                                     'aliyun.log.QueuedLogHandler',
                                     'level': 'INFO',
                                     'formatter': 'rawformatter',

                                     # custom args:
                                     'end_point': os.environ.get('ALIYUN_LOG_SAMPLE_ENDPOINT', 'cn-shanghai.log.aliyuncs.com'),
                                     'access_key_id': os.environ.get('ALIYUN_LOG_SAMPLE_ACCESSID', 'LTAISgWKc7klzmRq'),
                                     'access_key': os.environ.get('ALIYUN_LOG_SAMPLE_ACCESSKEY', '38qp74xFx0S9pcFnkN18Kfa31kdMyU'),
                                     'project': 'log-test-qc2019',
                                     'log_store': "log-store-qc2019"
                                     }
                     },
        'loggers': {'sls': {'handlers': ['sls_handler', ],
                                   'level': 'INFO',
                                   'propagate': False}
                    }
        }

dict_conf = {'version': 1,
        'formatters': {'rawformatter': {'class': 'logging.Formatter',
                                        'format': '%(message)s'}
                       },
        'handlers': {'sls_handler': {'()':
                                     'aliyun.log.QueuedLogHandler',
                                     'level': 'INFO',
                                     'formatter': 'rawformatter',

                                     # custom args:
                                     'end_point': os.environ.get('ALIYUN_LOG_SAMPLE_ENDPOINT', 'cn-shanghai.log.aliyuncs.com'),
                                     'access_key_id': os.environ.get('ALIYUN_LOG_SAMPLE_ACCESSID', 'LTAISgWKc7klzmRq'),
                                     'access_key': os.environ.get('ALIYUN_LOG_SAMPLE_ACCESSKEY', '38qp74xFx0S9pcFnkN18Kfa31kdMyU'),
                                     'project': 'log-test-qc2019',
                                     'log_store': "log-store-qc2019",
                                     'extract_json': True
                                     }
                     },
        'loggers': {'sls': {'handlers': ['sls_handler', ],
                                   'level': 'INFO',
                                   'propagate': False}
                    }
        }


def log_text(text):
    logging.config.dictConfig(text_conf)

    # 使用
    logger = logging.getLogger('sls')
    logger.info(text)


def log_json(dict_item):
    logging.config.dictConfig(dict_conf)

    name = random.choice(['apple', 'amazon', 'alibaba'])

    logger = logging.getLogger('sls.{}'.format(name))
    logger.info(dict_item)


if __name__ == '__main__':

    for _ in range(10):

        log_json({'a': random.randint(0, 9), 'b': 'US', 'c': '美国'})
        log_json({'a': random.randint(0, 9), 'b': 'GB', 'c': '英国'})
        log_json({'a': random.randint(0, 9), 'b': 'CN', 'c': '中国',
                  'd': ['test', 'log', 'list']})