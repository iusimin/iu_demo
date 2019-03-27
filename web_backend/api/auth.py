import json
import falcon
from cl.utils import password
from web_backend.api import BaseApiResource
from web_backend.model.mongo.user import User
from datetime import datetime
from web_backend.model.redis_keys.session import Session
from web_backend.hooks.auth import login_required

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
            raise falcon.HTTPInvalidParam('HTTP param not valid')
        u = User.objects.filter(username=username_attempt).first()
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

class UserLogoutApi(BaseApiResource):
    @falcon.before(login_required)
    def on_post(self, req, resp):
        session = req.context['session']
        session.logout()
        resp.unset_cookie('session_id')
        resp.media = {
            'title': 'Logout Success',
        }