from web_backend.model.redis_keys import BaseRedisKey, redis_pipeline
from web_backend.model.mongo.user import User
import uuid
import walrus as w
from datetime import timedelta
from web_backend.lib.cache import instance_cache

GUEST_PREFIX = 'G_'

class Session(BaseRedisKey):
    __container__ = w.Hash

    @classmethod
    def options(cls):
        return cls.application.options['session']

    @classmethod
    def create_new_session(cls):
        key = uuid.uuid1().hex
        guest_uid = GUEST_PREFIX+key
        with redis_pipeline() as pipe:
            session_hash = cls(key).container(pipe)
            session_hash.update(
                user_id=guest_uid,
            )
            ttl = timedelta(seconds=cls.options()['guest_expire'])
            session_hash.expire(ttl)        
        return key

    @property
    @instance_cache()
    def snapshot(self):
        return self.container()
    
    def is_guest(self):
        user_id = self.snapshot.get('user_id').decode('utf-8')
        return user_id[:2] == 'G_' and len(user_id) == 34
    
    def is_valid(self):
        return self.key in self.db

    def get_user(self):
        if self.is_guest():
            return None
        return User.objects.filter(id=self.snapshot['user_id'])

    def login(self, user):
        # Update session user_id to login user and expire ttl
        with redis_pipeline() as pipe:
            session_hash = self.container(pipe)
            session_hash.update(
                user_id=str(user.id)
            )
            ttl = timedelta(seconds=self.options()['login_expire'])
            session_hash.expire(ttl)

    def logout(self):
        session_hash = self.container()
        del session_hash