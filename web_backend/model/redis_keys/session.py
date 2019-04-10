from web_backend.model.mongo.user import User
import uuid
import walrus as w
from datetime import timedelta, datetime
from cl.utils.cache import instance_cache
from web_backend.model.mongo.user import User
from cl.utils.redis import BaseRedisKey, redis_pipeline
import pickle

GUEST_PREFIX = 'G_'

class Session(BaseRedisKey):
    __container__ = w.Hash
    user = None

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
    def user(self):
        session_content = self.snapshot
        if 'user_cache' not in session_content or \
                int(session_content['user_expire']) < int(datetime.utcnow().strftime('%s')):
            user_expire = datetime.utcnow() + timedelta(seconds=self.options()['user_expire'])
            user_expire = user_expire.strftime('%s')
            user = User.objects.filter(
                id=session_content['user_id'].decode('utf-8')
            )[0]
            self.container().update(
                user_cache=pickle.dumps(user),
                user_expire=user_expire,
                user_permissions=pickle.dumps(user.get_permissions()),
            )
            return user
        else:
            return pickle.loads(session_content['user_cache'])
    
    @property
    def permissions(self):
        session_content = self.snapshot
        if 'user_permissions' not in session_content or \
                int(session_content['user_expire']) < int(datetime.utcnow().strftime('%s')):
            return self.user.get_permissions()
        else:
            return pickle.loads(session_content['user_permissions'])

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
        session_hash = self.container()
        del session_hash