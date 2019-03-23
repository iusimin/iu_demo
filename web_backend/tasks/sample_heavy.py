from web_backend.tasks import AbstractAsyncTaskFactory
import time

class SampleHeavyTasks(AbstractAsyncTaskFactory):
    @classmethod
    def init(cls, *args, **kwargs):
        super(SampleHeavyTasks, cls).init(*args, **kwargs)
        cls.sample = cls.bind_func(
            cls.sample,
        )
    
    @staticmethod
    def sample(task, x, y):
        print('{x}*{y}={z}'.format(
            x=x, y=y, z=x*y))