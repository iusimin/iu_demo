import json
import falcon
from cl.utils import password
from cl.backend.api import BaseApiResource
from web_backend.model.mongo.user import User
from web_backend.model.mongo.rbac import Role
from iu_mongo import errors as dberr
from web_backend.tasks.sample_light import SampleLightTasks
from web_backend.tasks.sample_heavy import SampleHeavyTasks
from web_backend.hooks.auth import login_required, permission_required
from cl.backend.hooks.validation import JsonSchema, UrlParamsSchema
from cl.backend.hooks.transform import add_list_index
from web_backend.model.mongo.rbac import Permission

def extract_params_object(req, resp, resource, params):
    if 'user_id' in params:
        user = User.find_one({
            'user_id': params['user_id']
        })
        if not user:
            raise falcon.HTTPNotFound(
                    title='User not found',
                    description='user_id=%s' % params['user_id'])
        req.context['api_user'] = user

class UserCollectionApi(BaseApiResource):
    @falcon.before(permission_required)
    def on_get(self, req, resp):
        all_users = User.find({})
        resp.media = [u.to_json_dict() for u in all_users]

    @falcon.before(JsonSchema('''
    type: object
    properties:
      username: { type: string }
      password: { type: string }
      email:
        type: string
        format: email
      phone_number: { type: string }
    required: [username, password, email, phone_number]
    '''))
    def on_post(self, req, resp):
        params = req.media
        try:
            username = params['username']
            pwd = params['password']
            email = params['email']
            phone = params['phone_number']
        except KeyError:
            raise falcon.HTTPBadRequest('Bad input body')

        e_password = password.encrypt_password(pwd)
        try:
            u = User(
                username=username,
                password=e_password,
                email=email,
                phone_number=phone,
            )
            u.save()
            resp.status = falcon.HTTP_201
            resp.media = {
                'id': str(u.id),
                'username': str(u.username),
            }
        except dberr.NotUniqueError as e:
            raise falcon.HTTPBadRequest('User already exists1111')

class UserApi(BaseApiResource):
    URL_PARAMS_SCHEMA = UrlParamsSchema('''
    type: object
    properties:
      user_id:
        type: string
        minLength: 24
        maxLength: 24
    ''')

    @falcon.before(extract_params_object)
    @falcon.before(permission_required)
    def on_get(self, req, resp, user_id):
        u = req.context['api_user']
        ret = u.to_json_dict()
        roles = u.get_roles()
        ret['roles'] = [r.to_json_dict() for r in roles]
        for r in ret['roles']:
            r.pop('permissions_all')
        resp.media = ret
    
    @falcon.before(extract_params_object)
    @falcon.before(permission_required)
    def on_delete(self, req, resp, user_id):
        u = req.context['api_user']
        u.delete()
        resp.media = {
            'title': 'Success',
            'id': user_id,
        }

class UserRoleCollectionApi(BaseApiResource):
    URL_PARAMS_SCHEMA = UrlParamsSchema('''
    type: object
    properties:
      user_id:
        type: string
        minLength: 24
        maxLength: 24
    ''')

    @falcon.before(extract_params_object)
    @falcon.before(permission_required)
    def on_get(self, req, resp, user_id):
        u = req.context['api_user']
        roles = u.get_roles()
        ret = [r.to_json_dict() for r in roles]
        for r in ret:
            r.pop('permissions_all')
        resp.media = ret
    
    @falcon.before(extract_params_object)
    @falcon.before(JsonSchema('''
    anyOf:
      - type: string
      - type: array
        items:
          type: string
    '''))
    @falcon.before(permission_required)
    def on_post(self, req, resp, user_id):
        u = req.context['api_user']
        role_names = req.media
        if isinstance(role_names, str):
            role_names = [role_names]
        for r in role_names:
            if r not in u.role_names:
                u.role_names.append(r)
        u.save()
        resp.media = role_names
        resp.status = falcon.HTTP_201
    
    @falcon.before(extract_params_object)
    @falcon.before(JsonSchema('''
    type: array
    items: { type: string }
    '''))
    @falcon.before(permission_required)
    def on_put(self, req, resp, user_id):
        u = req.context['api_user']
        role_names = req.media
        u.role_names = role_names
        u.save()
        resp.media = role_names

class UserRoleApi(BaseApiResource):
    URL_PARAMS_SCHEMA = UrlParamsSchema('''
    type: object
    properties:
      user_id:
        type: string
        minLength: 24
        maxLength: 24
      role_name: { type: string }
    ''')
    @falcon.before(extract_params_object)
    @falcon.before(permission_required)
    def on_delete(self, req, resp, user_id, role_name):
        user = req.context['api_user']
        if role_name not in user.role_names:
            raise falcon.HTTPBadRequest(
                'User %s does not have role %s' % (user_id, role_name)
            )
        user.role_names.remove(role_name)
        user.save()
        resp.media = {
            'title': 'Success',
            'user_id': user_id,
            'role_name': role_name,
        }

class UserPermissionCollectionApi(BaseApiResource):
    URL_PARAMS_SCHEMA = UrlParamsSchema('''
    type: object
    properties:
      user_id:
        type: string
        minLength: 24
        maxLength: 24
    ''')

    @falcon.after(add_list_index)
    @falcon.before(extract_params_object)
    @falcon.before(permission_required)
    def on_get(self, req, resp, user_id):
        user = req.context['api_user']
        resp.media = [
            p.to_json_dict() for p in user.permissions
        ]
    
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
    def on_post(self, req, resp, user_id):
        user = req.context['api_user']
        params = req.media
        if isinstance(params, dict):
            params = [params]
        permissions = []
        for p in params:
            permission = Permission(
                allow=p['allow'],
                resource=p['resource'],
                actions=p['actions']
            )
            if permission not in user.permissions:
                user.permissions.append(permission)
        user.save()
        resp.media = [
            p.to_json_dict() for p in user.permissions
        ]

class UserPermissionApi(BaseApiResource):
    @falcon.after(add_list_index)
    @falcon.before(extract_params_object)
    @falcon.before(permission_required)
    def on_get(self, req, resp, user_id, permission_id):
        user = req.context['api_user']
        resp.media = [
            p.to_json_dict() for p in user.permissions
        ]
    
    @falcon.before(extract_params_object)
    @falcon.before(permission_required)
    def on_delete(self, req, resp, user_id, permission_id):
        user = req.context['api_user']
        user.permissions.pop(permission_id)
        user.save()
        resp.media = {
            'title': 'Success',
            'user_id': user_id,
            'permission_id': permission_id,
        }