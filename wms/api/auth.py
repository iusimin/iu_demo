import json
from datetime import datetime

import falcon

from cl.backend.api import BaseApiResource
from cl.backend.hooks.validation import JsonSchema
from cl.utils import password
from wms.hooks.auth import login_required, permission_required
from wms.model.mongo.user import User
from wms.model.redis_keys.session import Session


class UserLoginApi(BaseApiResource):
    @falcon.before(login_required)
    def on_get(self, req, resp):
        session = req.context['session']
        session_dict = session.snapshot
        resp.media = {
            'user_id': session_dict.get('user_id').decode('utf-8'),
            'is_guest': session.is_guest(),
        }

    def on_post(self, req, resp):
        params = req.media
        try:
            username_attempt = params['username']
            password_attempt = params['password']
        except KeyError:
            raise falcon.HTTPInvalidParam('username or password is missing.', '')
        u = User.find_one({
            'username': username_attempt
        })
        if not u:
            raise falcon.HTTPUnauthorized('User %(username)s not exists' % params)
        if not password.verify_password(u.password, password_attempt):
            raise falcon.HTTPUnauthorized('Incorrect password')
        
        session = req.context['session']
        session.login(u)
        resp.media = {
            'title': 'Login Success',
            'user_id': str(u.id),
            'username': str(u.username),
        }
