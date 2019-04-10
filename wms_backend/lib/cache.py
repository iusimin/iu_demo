from functools import wraps
from datetime import datetime
import pickle

def instance_cache(timeout=None):
    """ Decorator to the result of a function call inside a class
    Cache value will be store inside __instance_cache__ field of the class or instance
    
    Parameters:
        timeout (timedelta): when the cache value become invalid
    
    Returns:
        wrapped function
    """
    def __decorate(f):
        @wraps(f)
        def __wraps(self, *args, **kwargs):
            cache_dict_name = '__instance_cache__'
            if not hasattr(self, cache_dict_name):
                setattr(self, cache_dict_name, {})
            cache_dict = self.__instance_cache__
            f_key = pickle.dumps([f.__name__, args, kwargs])
            if timeout:
                expire_ts = datetime.utcnow() + timeout
            else:
                expire_ts = None
            if f_key not in cache_dict:
                # Cache missing
                cache_dict[f_key] = {
                    'expire_ts': expire_ts,
                    'result': f(self, *args, **kwargs),
                }
            cached_data = cache_dict[f_key]
            if cached_data['expire_ts'] is not None and \
                    cached_data['expire_ts'] < datetime.utcnow():
                # Cache expire
                cache_dict[f_key] = {
                    'expire_ts': expire_ts,
                    'result': f(self, *args, **kwargs),
                }
                cached_data = cache_dict[f_key]
            return cached_data['result']
        return __wraps
    return __decorate