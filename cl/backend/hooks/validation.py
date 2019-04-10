import falcon
import jsonschema
import yaml
import json

class JsonSchema(object):
    def __init__(self, schema=None, target='content',
            title='Request data failed validation'):
        if isinstance(schema, str):
            self.schema = yaml.safe_load(schema)
        elif isinstance(schema, dict):
            self.schema = schema
        else:
            raise falcon.HTTPInternalServerError(
                'Bad JSON schema'
            )
        if target not in ['content', 'params']:
            raise falcon.HTTPInternalServerError(
                'Invalid schema target'
            )
        self.target = target
        self.title=title
    
    def __call__(self, req, resp, resource, params):
        if self.target == 'params':
            inst = params
        elif self.target == 'content':
            if req.method in ['POST', 'PUT', 'PATCH']:
                inst = req.media
            elif req.method in ['GET']:
                inst = req.params
        else:
            raise falcon.HTTPInternalServerError(
                'Method %s does not support data validation' % req.method,
            )
        try:
            jsonschema.validate(
                inst, self.schema,
                format_checker=jsonschema.FormatChecker()
            )
        except jsonschema.ValidationError as e:
            raise falcon.HTTPBadRequest(
                self.title,
                description=e.message,
            )

class UrlParamsSchema(JsonSchema):
    def __init__(self, schema=None):
        super(UrlParamsSchema, self).__init__(
            schema=schema,
            target='params',
            title='URL param failed validation'
        )