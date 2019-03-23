from web_backend.api import all as a

API_ROUTER = [
    ('/api/user/{user_id}', a.UserApi),
    ('/api/user', a.UserCollectionApi),
    ('/api/sleep', a.SleepApi),
    ('/api/worker_test', a.WorkerTestApi),
]