import pickle
import uuid
from datetime import datetime, timedelta
import walrus as w

from cl.utils.redis import BaseRedisKey, redis_pipeline
from demo.lib.cache import instance_cache
from demo.model.mongo.user import User

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
    
    @property
    def user_id(self):
        session_content = self.snapshot
        if self.is_guest():
            return session_content.get('user_id').decode('utf-8')
        return str(self.user.id) if self.user else None

    @property
    def permissions(self):
        session_content = self.snapshot
        return self.user.get_permissions() if self.user else []

    @property
    def user(self):
        session_content = self.snapshot
        if self.is_guest():
            return None
        if 'user_cache' not in session_content or \
                int(session_content['user_expire']) < int(datetime.utcnow().strftime('%s')):
            user_expire = datetime.utcnow() + timedelta(seconds=self.options()['user_expire'])
            user_expire = user_expire.strftime('%s')
            user = User.by_id(session_content['user_id'].decode('utf-8'))
            self.container().update(
                user_cache=pickle.dumps(user),
                user_expire=user_expire,
                user_permissions=pickle.dumps(user.get_permissions()),
            )
            return user
        else:
            return pickle.loads(session_content['user_cache'])

    def expire_user(self):
        self.container().update(
            user_expire=datetime.utcnow().strftime('%s')
        )
    
    def is_guest(self):
        user_id = self.snapshot.get('user_id').decode('utf-8')
        return user_id[:2] == 'G_' and len(user_id) == 34
    
    def is_valid(self):
        return self.key in self.db

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
        self.delete()