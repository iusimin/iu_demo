import falcon
import jsonschema
import yaml
import json

class JsonSchema(object):
    def __init__(self, schema, target='content',
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
        self.title = title
    
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

class QuerySchema(JsonSchema):
    '''
    '''
    ALL_OPS = [ '$lt', '$gt', '$ne', '$lte', '$gte', '$exists']
    ALL_COMBINES = [ '$and', '$or' ]
    DEFAULT_MAX_LIMIT = 100
    
    def __list_to_pattern(self, l):
        if not l:
            return '.*'
        res = '|'.join(l)
        return '(%s)' % res

    def __init__(self, schema, fields=[],
            allowed_ops=ALL_OPS, allowed_combines=ALL_COMBINES,
            max_limit=DEFAULT_MAX_LIMIT, target='content',
            title='Request data failed validation'):
        schema = yaml.safe_load(schema)
        tdef_dict = {}
        try:
            assert schema.get('type') == 'object'
            assert isinstance(schema.get('properties'), dict)
            # query_ops + query_items
            item_props = {}
            for fname, fdef in schema.get('properties').items():
                assert len(fdef) == 1 and 'type' in fdef
                ftype = fdef['type']
                tdef_key = 'query_ops_%s' % ftype
                item_props.update({
                    fname: {
                        'oneOf': [
                            {'type': ftype},
                            {'$ref': '#/definitions/%s' % tdef_key},
                        ]
                    }
                })
                op_props = {}
                for op in allowed_ops:
                    if op == '$exists':
                        op_props.update({
                            op: {
                                'type': 'boolean'
                            }
                        })
                    else:
                        op_props.update({
                            op: {
                                'type': ftype
                            }
                        })
                
                tdef_dict.update({
                    tdef_key: {
                        'type': 'object',
                        'properties': op_props,
                        'additionalProperties': False,
                    }
                })
            tdef_dict.update({
                'query_items': {
                    'type': 'object',
                    'properties': item_props,
                    'additionalProperties': False,
                    'required': schema.get('required', [])
                }
            })
            # query_combines
            cb_props = {}
            for cb in allowed_combines:
                cb_props.update({
                    cb: {
                        'type': 'array',
                        'items': {
                            'oneOf': [
                                {'$ref': "#/definitions/query_items"},
                                {'$ref': "#/definitions/query_combines"},
                            ]
                        }
                    }
                })
            tdef_dict.update({
                'query_combines': {
                    'type': 'object',
                    'properties': cb_props,
                    'additionalProperties': False,
                }
            })
            # body
            # Checking and applying fields
            allowed_fields = [f['name'] for f in fields]
            allowed_sort = [f['name'] for f in fields if f.get('sortable')]
            converted_schema = {}
            body_properties = {
                'query': {
                    'anyOf': [
                        {'$ref': '#/definitions/query_items'},
                        {'$ref': '#/definitions/query_combines'},
                    ]
                },
                'limit': {
                    'type': 'integer',
                    'minimum': 1,
                    'maximum': max_limit,
                },
                'skip': {
                    'type': 'integer',
                    'minimum': 0,
                },
                'sort': { # [(field, order)]
                    'type': 'array',
                    'items': {
                        'type': 'array',
                        'items': [
                            {
                                'type': 'string',
                                'pattern': self.__list_to_pattern(allowed_sort)
                            },
                            {
                                'type': 'integer',
                                'minimum': -1,
                                'maximum': 1,
                            }
                        ]
                    }
                },
                'fields': {
                    'type': 'array',
                    'items': {
                        'type': 'string',
                        'pattern': self.__list_to_pattern(allowed_fields)
                    },
                }
            }
            converted_schema.update({
                'definitions': tdef_dict,
                'type': 'object',
                'properties': body_properties,
                'required': ['query'],
                'additionalProperties': False,
            })
        except AssertionError:
            raise falcon.HTTPInternalServerError(
                'Bad JSON schema'
            )
        self.schema = converted_schema
        self.target = target
        self.title = title

    def __call__(self, req, resp, resource, params):
        req.context['q'] = req.media
        super(QuerySchema, self).__call__(req, resp, resource, params)
