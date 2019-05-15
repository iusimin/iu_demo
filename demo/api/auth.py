import json
import falcon
from cl.utils import password
from cl.backend.api import BaseApiResource
from demo.model.mongo.user import User
from datetime import datetime
from demo.model.redis_keys.session import Session
from demo.hooks.auth import login_required, permission_required
from cl.backend.hooks.validation import JsonSchema

class UserLoginApi(BaseApiResource):
    def on_get(self, req, resp):
        session = req.context['session']
        permissions = session.permissions
        if session.user:
            username = session.user.username
        else:
            username = 'Guest'
        resp.media = {
            'user_id': str(session.user_id),
            'username': username,
            'permissions': [
                p.to_json_dict() for p in permissions
            ],
            'is_guest': session.is_guest(),
        }

    @falcon.before(JsonSchema('''
    type: object
    properties:
      username: { type: string }
      password: { type: string }
    required: [username, password]
    '''))
    def on_post(self, req, resp):
        params = req.media
        try:
            username_attempt = params['username']
            password_attempt = params['password']
        except KeyError:
            raise falcon.HTTPInvalidParam('HTTP param not valid')
        u = User.find_one({
            'username': username_attempt
        })
        if not u:
            raise falcon.HTTPUnauthorized('User %(username)s not exists' % params)
        if not password.verify_password(u.password, password_attempt):
            raise falcon.HTTPUnauthorized('Incorrect password')
        
        session = req.context['session']
        session.login(u)
        permissions = u.get_permissions()
        resp.media = {
            'title': 'Login Success',
            'user_id': str(u.id),
            'username': str(u.username),
            'permissions': [
                p.to_json_dict() for p in permissions
            ],
        }
    
    @falcon.before(login_required)
    def on_delete(self, req, resp):
        session = req.context['session']
        session.logout()
        resp.unset_cookie('session_id')
        resp.media = {
            'title': 'Logout Success',
        }

class SessionCollectionApi(BaseApiResource):
    @falcon.before(permission_required)
    def on_get(self, req, resp):
        session = req.context['session']
        session_content = session.snapshot
        permissions = session.permissions
        resp.media = {
            'user_id': session_content['user_id'].decode('utf-8'),
            'user_expire': str(
                datetime.fromtimestamp(int(session_content['user_expire']))
            ) if 'user_expire' in session_content else 'N/A',
            'session_ttl': session.ttl(),
            'permissions': [
                p.to_json_dict() for p in permissions
            ]
        }

    @falcon.before(login_required)
    def on_expireUserCache(self, req, resp):
        session = req.context['session']
        params = req.media
        session.expire_user()
        session_content = session.snapshot
        resp.media = {
            'user_id': session_content['user_id'].decode('utf-8'),
            'user_expire': str(
                datetime.fromtimestamp(int(session_content['user_expire']))
            ),
            'session_ttl': session.ttl(),
        }