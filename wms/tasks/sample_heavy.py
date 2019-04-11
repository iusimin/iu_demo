from wms.tasks import AbstractAsyncTaskFactory, async_task
import time

class SampleHeavyTasks(AbstractAsyncTaskFactory):
    @async_task()
    def sample(task, x, y):
        print('{x}*{y}={z}'.format(
            x=x, y=y, z=x*y))