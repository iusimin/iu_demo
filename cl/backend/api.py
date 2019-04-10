import falcon
from functools import wraps

def get_all_apis(a):
    res = []
    for member in a.__dict__.values():
        if not hasattr(member, '__bases__'):
            continue
        if BaseApiResource in member.__bases__:
            res.append(member)
    return res

def convert_custom_verb_pattern(uri_pattern):
    if uri_pattern.endswith('/'):
        uri_pattern = uri_pattern[:-1]
    uri_pattern += ':{custom_verb}'
    return uri_pattern

class BaseApiResource(object):
    DEFAULT_RESETFUL_FUNCTION = True
    ENABLE_CUSTOM_VERB = True
    URL_PARAMS_SCHEMA = None

    def __init__(self, application, custom_verb=False):
        self.application = application
        self.custom_verb=custom_verb
        # Monkey patch on_post function for custom_verb
        if self.custom_verb:
            setattr(self, 'on_post', self.route_custom_verb)
            for verb in ['get', 'put', 'patch', 'delete']:
                fname = 'on_'+verb
                setattr(self, fname, self.method_not_allowed)

    def method_not_allowed(self, req, resp, *args, **kwargs):
        raise falcon.HTTPMethodNotAllowed(allowed_methods=['POST'])

    def route_custom_verb(self, req, resp, custom_verb, *args, **kwargs):
        fname = 'on_%s' % custom_verb
        if not hasattr(self, fname):
            raise falcon.HTTPNotFound()
        return getattr(self, fname)(req, resp, *args, **kwargs)