from cl.backend.tasks import AbstractAsyncTaskFactory, async_task
import time

class SampleHeavyTasks(AbstractAsyncTaskFactory):
    @classmethod
    @async_task()
    def sample(cls, task, x, y):
        print(cls)
        print(task)
        print('{x}*{y}={z}'.format(
            x=x, y=y, z=x*y))