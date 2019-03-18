from threading import local
import logging
import os

logger = logging.getLogger('cl.utils')

class SingletonMixin(object):

    @classmethod
    def _instance_name(cls):
        if hasattr(cls, '_disable_fork_protection'):
            identifier = 0
        else:
            identifier = os.getpid()
        return "_%s_Singleton_%d" % (cls.__name__, identifier)

    @classmethod
    def instance(cls, *args, **kwargs):
        attr_name = cls._instance_name()
        if hasattr(cls, attr_name) and (args or kwargs):
            logger.warning('Arguments are passed to instance(), but '
               'pre-constructed instance is returned as singleton.')
        if not hasattr(cls, attr_name):
            instance = cls(*args, **kwargs)
            setattr(cls, attr_name, instance)
        return getattr(cls, attr_name)