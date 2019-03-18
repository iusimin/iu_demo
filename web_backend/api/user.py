import json
import falcon
from cl.utils import password
from web_backend.api.base import BaseApiResource
from web_backend.model.user import User
from mongoengine import errors as dberr

class UserCollectionApi(BaseApiResource):
    def on_get(self, req, resp):
        all_users = User.objects
        resp.body = json.dumps(
            [{
                'id': str(u.id),
                'username': u.username,
                'password': u.password,
                'email': u.email,
                'phone_number': u.phone_number,
            } for u in all_users],
            ensure_ascii=False)
        resp.status = falcon.HTTP_200

    def on_post(self, req, resp):
        try:
            post_body = json.loads(req.stream.read().decode('utf-8'))
            username = post_body['username']
            pwd = post_body['password']
            email = post_body['email']
            phone = post_body['phone_number']
        except KeyError:
            raise falcon.HTTPBadRequest('Bad input body')

        e_password = password.encrypt_password(pwd)
        try:
            User(
                username=username,
                password=e_password,
                email=email,
                phone_number=phone,
            ).save()
            resp.status = falcon.HTTP_201
            resp.body = json.dumps({
                'result': 'Success'
            }, ensure_ascii=False)
        except dberr.NotUniqueError as e:
            raise falcon.HTTPBadRequest('User already exists')

class UserApi(BaseApiResource):
    def on_get(self, req, resp, user_id):
        ''' Getting user meta info '''
        e_password = password.encrypt_password(user_id)
        resp.body = json.dumps({
            'user_id': user_id,
            'password': e_password,
        }, ensure_ascii=False)
        resp.status = falcon.HTTP_200

class SleepApi(BaseApiResource):
    def on_get(self, req, resp):
        res = str(User.objects(__raw__={
            '$where': 'sleep(10000) || true'
        }))
        # from mongoengine.connection import get_db
        # db = get_db()
        # res = str(db.command('sleep (10)'))
        resp.body = json.dumps(res, ensure_ascii=False)
        resp.status = falcon.HTTP_200