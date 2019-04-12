from demo.model.mongo.rbac import Role, Permission
from cl.backend.api import BaseApiResource
from cl.backend.hooks.validation import JsonSchema
from demo.hooks.auth import permission_required
from cl.backend.hooks.transform import add_list_index
from iu_mongo import errors as dberr
import falcon
import json
from bson import ObjectId

def extract_params_object(req, resp, resource, params):
    if 'role_name' in params:
        role = Role.find_one({
            'name': params['role_name']
        })
    else:
        return
    if 'permission_id' in params:
        if params['permission_id'] >= len(role.permissions):
            raise falcon.HTTPBadRequest(
                    'Permission index out of range. Total: %s' 
                    % len(role.permissions))
        else:
            req.context['permission'] = role.permissions[params['permission_id']]
    if 'parent_name' in params:
        if params['parent_name'] not in role.parents:
            raise falcon.HTTPBadRequest(
                    '%s is not the parent of current role' 
                    % len(role.parents))
    if not role:
        raise falcon.HTTPNotFound(
                title='Role not found',
                description='role_name=%s' % params['role_name'])
    req.context['role'] = role

class RoleCollectionApi(BaseApiResource):
    @falcon.before(permission_required)
    def on_get(self, req, resp):
        roles = Role.find({})
        resp.media = [{
            'id': str(r.id),
            'name': r.name,
            'description': r.description,
        } for r in roles]

    @falcon.before(JsonSchema('''
    definitions:
      permission:
        type: object
        properties:
          allow: { type: boolean }
          resource: { type: string }
          actions:
            type: array
            items: { type: string }
            pattern: (GET|POST|PUT|PATCH|DELETE)
        required: [allow, resource, actions]
      role:
        type: object
        properties:
          name: { type: string }
          description: { type: string }
          parents:
            type: array
            items:
              type: string
              minLength: 24
              maxLength: 24
          permissions:
            type: array
            items:
              $ref: "#/definitions/permission"
        required: [name, permissions]
    
    anyOf:
      - $ref: "#/definitions/role"
      - type: array
        items:
          $ref: "#/definitions/role"
    '''))
    @falcon.before(permission_required)
    def on_post(self, req, resp):
        params = req.media
        if isinstance(params, dict):
            params = [params]
        roles = []
        for param in params:
            permissions = []
            for p in param['permissions']:
                actions = [Permission.Action.name_to_num(
                    a.upper()
                ) for a in p['actions']]
                permissions.append(Permission(
                    resource=p['resource'],
                    allow=p['allow'],
                    actions=actions,
                ))
            roles.append(Role(
                name=param['name'],
                description=param.get('description'),
                parents=param.get('parents', []),
                permissions=permissions,
            ))
        try:
            with Role.bulk() as bulk_context:
                for r in roles:
                    r.bulk_save(bulk_context)
        except dberr.NotUniqueError as e:
            raise falcon.HTTPBadRequest(
                'Role name already exists.'
            )
        ret_value = [r.to_json_dict() for r in roles]
        if len(ret_value) == 0:
            resp.media = ret_value[0]
        else:
            resp.media = ret_value
        resp.status = falcon.HTTP_201

class RoleApi(BaseApiResource):
    @falcon.before(extract_params_object)
    @falcon.before(permission_required)
    def on_get(self, req, resp, role_name):
        role = req.context['role']
        resp.media = role.to_json_dict()

    @falcon.before(extract_params_object)
    @falcon.before(JsonSchema('''
    type: object
    properties:
      name: { type: string }
      description: { type: string }
    '''))
    @falcon.before(permission_required)
    def on_patch(self, req, resp, role_name):
        params = req.media
        role = req.context['role']
        for k, v in params.items():
            setattr(role, k, v)
        role.save()
        resp.media = role.to_json_dict()

    @falcon.before(extract_params_object)
    @falcon.before(permission_required)
    def on_delete(self, req, resp, role_name):
        role = req.context['role']
        role.delete()
        resp.media = {
            'title': 'Success',
            'id': role_name,
        }

class RolePermissionCollectionApi(BaseApiResource):
    @falcon.after(add_list_index)
    @falcon.before(extract_params_object)
    @falcon.before(permission_required)
    def on_get(self, req, resp, role_name):
        role = req.context['role']
        resp.media = [p.to_json_dict() for p in role.permissions]

    @falcon.after(add_list_index)
    @falcon.before(extract_params_object)
    @falcon.before(JsonSchema('''
    definitions:
      permission:
        type: object
        properties:
          allow: { type: boolean }
          resource: { type: string }
          actions:
            type: array
            items: { type: string }
            pattern: (GET|POST|PUT|PATCH|DELETE)
        required: [allow, resource, actions]
    
    anyOf:
      - type: array
        items:
          $ref: "#/definitions/permission"
      - $ref: "#/definitions/permission"
    '''))
    @falcon.before(permission_required)
    def on_post(self, req, resp, role_name):
        role = req.context['role']
        params = req.media
        if isinstance(params, dict):
            params = [params]
        resp.media = []
        permission_resources = [p.resource for p in role.permissions]
        for p in params:
            if p['resource'] not in permission_resources:
                permission = Permission(
                    allow=p['allow'],
                    resource=p['resource'],
                    actions=[
                        Permission.Action.name_to_num(a)
                            for a in p['actions']
                    ]
                )
                role.permissions.append(permission)
                permission_resources.append(p)
        role.save()
        resp.media = [p.to_json_dict() for p in role.permissions]
        resp.status = falcon.HTTP_201

    @falcon.before(extract_params_object)
    @falcon.before(JsonSchema('''
    definitions:
      permission:
        type: object
        properties:
          allow: { type: boolean }
          resource: { type: string }
          actions:
            type: array
            items: { type: string }
            pattern: (GET|POST|PUT|PATCH|DELETE)
        required: [allow, resource, actions]
    
    type: array
    items:
      $ref: "#/definitions/permission"
    '''))
    @falcon.before(permission_required)
    def on_put(self, req, resp, role_name):
        role = req.context['role']
        params = req.media
        resp.media = []
        permissions = []
        for p in params:
            permission = Permission(
                allow=p['allow'],
                resource=p['resource'],
                actions=[
                    Permission.Action.name_to_num(a)
                        for a in p['actions']
                ]
            )
            if permission in role.permissions:
                raise falcon.HTTPBadRequest(
                    'Duplicate permission %s' % p
                )
            permissions.append(permission)
        role.permissions = permissions
        role.save()
        resp.media = [ p.to_json_dict() for p in role.permissions ]

class RolePermissionApi(BaseApiResource):
    @falcon.before(extract_params_object)
    @falcon.before(permission_required)
    def on_get(self, req, resp, role_name, permission_id):
        role = req.context['role']
        permission = req.context['permission']
        resp.media = permission.to_json_dict()
    
    @falcon.before(extract_params_object)
    @falcon.before(JsonSchema('''
    type: object
    properties:
      allow: { type: boolean }
      resource: { type: string }
      actions:
        type: array
        items: { type: string }
        pattern: (GET|POST|PUT|PATCH|DELETE)
    required: [allow, resource, actions]
    '''))
    @falcon.before(permission_required)
    def on_put(self, req, resp, role_name, permission_id):
        role = req.context['role']
        params = req.media
        role.permissions[permission_id] = Permission(
            allow=params['allow'],
            resource=params['resource'],
            actions=[
                Permission.Action.num_to_name()[a] for a in params['actions']
            ]
        )
        role.save()
        permission = role.permissions[permission_id]
        resp.media = permission.to_json_dict()

    @falcon.before(extract_params_object)
    @falcon.before(permission_required)
    def on_delete(self, req, resp, role_name, permission_id):
        role = req.context['role']
        role.permissions.pop(permission_id)
        role.save()
        resp.media = {
            'title': 'Success',
            'role_name': role_name,
            'permission_id': permission_id,
        }

class RoleParentCollectionApi(BaseApiResource):
    @falcon.before(extract_params_object)
    @falcon.before(permission_required)
    def on_get(self, req, resp, role_name):
        role = req.context['role']
        parents = Role.find({
            'name': {
                '$in': role.parents,
            }
        })
        resp.media = [ p.to_json_dict() for p in parents ]

    @falcon.before(extract_params_object)
    @falcon.before(JsonSchema('''
    definitions:
      parent:
        type: string
        minLength: 24
        maxLength: 24
    
    anyOf:
      - type: array
        items:
          $ref: "#/definitions/parent"
      - $ref: "#/definitions/parent"
    '''))
    @falcon.before(permission_required)
    def on_post(self, req, resp, role_name):
        role = req.context['role']
        params = req.media
        if isinstance(params, str):
            params = [params]
        resp.media = []
        
        for p in params:
            if ObjectId(p) not in role.parents:
                role.parents.append(p)
        role.save()
        resp.media = [str(p) for p in role.parents]
        resp.status = falcon.HTTP_201
    
    @falcon.before(extract_params_object)
    @falcon.before(JsonSchema('''
    definitions:
      parent:
        type: string
        minLength: 24
        maxLength: 24
    
    type: array
    items:
      $ref: "#/definitions/parent"
    '''))
    @falcon.before(permission_required)
    def on_put(self, req, resp, role_name):
        role = req.context['role']
        params = req.media
        role.parents = params
        role.save()
        resp.media = [str(p) for p in role.parents]

class RoleParentApi(BaseApiResource):
    @falcon.before(extract_params_object)
    @falcon.before(permission_required)
    def on_get(self, req, resp, role_name, parent_name):
        role = req.context['role']
        parent = Role.find_one({
            'name': parent_name
        })
        resp.media = parent.to_json_dict()

    @falcon.before(extract_params_object)
    @falcon.before(permission_required)
    def on_delete(self, req, resp, role_name, parent_name):
        role = req.context['role']
        role.parents.remove(parent_name)
        role.save()
        resp.media = {
            'title': 'Success',
            'role_name': role_name,
            'parent_name': parent_name,
        }