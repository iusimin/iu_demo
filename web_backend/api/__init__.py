import falcon
from functools import wraps

class BaseApiResource(object):
    def __init__(self, application):
        self.application = application