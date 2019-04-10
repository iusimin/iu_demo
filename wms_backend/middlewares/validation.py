from wms_backend.hooks.validation import JsonSchema

class RequireJSONMiddleware(object):
    def process_request(self, req, resp):
        if not req.client_accepts_json:
            raise falcon.HTTPNotAcceptable(
                'This API only supports responses encoded as JSON.')

        if req.method in ('POST', 'PUT'):
            if 'application/json' not in req.content_type:
                raise falcon.HTTPUnsupportedMediaType(
                    'This API only supports requests encoded as JSON.')

class RequestValidationMiddleware(object):
    def process_resource(self, req, resp, resource, params):
        ''' Validated input param schema using JSON Schema
        '''
        if getattr(resource, 'URL_PARAMS_SCHEMA', None):
            resource.URL_PARAMS_SCHEMA(
                req, resp, resource, params
            )