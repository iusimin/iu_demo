from web_backend.tasks import AbstractCronTaskFactory
import time

# TODO - add celery beat service
class SampleCronTask(AbstractCronTaskFactory):
    @classmethod
    def init(cls, *args, **kwargs):
        super(SampleCronTask, cls).init(*args, **kwargs)
        cls.sample = cls.bind_func(
            cls.sample,
        )
    
    @staticmethod
    def sample(task, x, y):
        print('This is a cron job: {x}+{y}={z}'.format(
            x=x, y=y, z=x+y))