from wms.tasks import AbstractAsyncTaskFactory, async_task
import time

class SampleLightTasks(AbstractAsyncTaskFactory):
    @async_task(retry_kwargs={
        'max_retries': 1,
    })
    def sample(task, x, y):
        print('{x}+{y}={z}'.format(
            x=x, y=y, z=x+y))