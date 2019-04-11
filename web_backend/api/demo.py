from cl.backend.api import BaseApiResource
from web_backend.model.mongo.user import User
from web_backend.tasks.sample_light import SampleLightTasks
from web_backend.tasks.sample_heavy import SampleHeavyTasks

class DemoApi(BaseApiResource):
    def on_mongoSleep(self, req, resp):
        sleep_seconds = req.media['seconds']
        res = User.find({
            '$where': 'sleep(%s) || true' % (sleep_seconds*1000)
        })
        resp.media = {
            'title': '%s seconds sleep.' % sleep_seconds
        }
    
    def on_publishAsyncTask(self, req, resp):
        light_num = req.media.get('light', 0)
        heavy_num = req.media.get('heavy', 0)
        for i in range(light_num):
            SampleLightTasks.sample.delay(2, 3)
        for i in range(heavy_num):
            SampleHeavyTasks.sample.delay(2, 3)
        resp.media = {
            'heavy_task_queued': heavy_num,
            'light_task_queued': light_num,
        }
        