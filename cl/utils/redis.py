import inflection
from contextlib import contextmanager
import redis
from datetime import datetime, timedelta

class BaseRedisKey(object):
    __namespace__ = None
    __container__ = None

    @classmethod
    def init(cls, application):
        cls.application = application
        cls.db = application.redis_db
        cls.conn = application.redis_conn
    
    def __init__(self, raw_key):
        if self.__namespace__ is None:
            self.__namespace__ = inflection.underscore(self.__class__.__name__)
        self.key = '%s$%s' % (self.__namespace__, raw_key)
        
    def key_exists(self):
        return self.key in self.db
    
    def container(self, pipeline=None):
        if self.__container__ is None:
            raise NotImplementedError('Container is not defined')
        if pipeline is not None:
            source = pipeline
        else:
            source = self.db
        return self.__container__(source, self.key)
    
    def ttl(self):
        if self.__container__ is None:
            raise NotImplementedError('Container is not defined')
        return self.conn.ttl(self.key)


@contextmanager
def redis_pipeline(db=None):
    '''Provide a pipeline scope around a series of redis operations.'''
    if db is None:
        db = BaseRedisKey.db
    pipeline = db.pipeline()
    yield pipeline
    pipeline.execute()