from web_backend.api import BaseApiResource
from web_backend.model.mongo.user import User

class DemoApi(BaseApiResource):
    def on_mongoSleep(self, req, resp):
        sleep_seconds = req.media['seconds']
        res = str(User.objects(__raw__={
            '$where': 'sleep(%s) || true' % (sleep_seconds*1000)
        }))
        resp.media = {
            'title': '%s seconds sleep.' % sleep_seconds
        }
    
    def on_publishAsyncTask(self, req, resp):
        light_num = req.media['light']
        heavy_num = req.media['heavy']
        for i in range(light_num):
            SampleLightTasks.sample.delay(2, 3)
        for i in range(heavy_num):
            SampleHeavyTasks.sample.delay(2, 3)
        resp.media = {
            'heavy_task_queued': heavy_num,
            'light_task_queued': light_num,
        }
        