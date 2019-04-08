#encoding: utf8
import logging, logging.config, os

# 配置
conf = {'version': 1,
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
logging.config.dictConfig(conf)

# 使用
logger = logging.getLogger('sls')
logger.info("Hello world")