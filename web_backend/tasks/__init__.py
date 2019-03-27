from functools import wraps
import inflection
from celery import Task
from celery.exceptions import TaskPredicate, MaxRetriesExceededError
import logging
import requests
import random

class AbstractAsyncTaskFactory(object):
    DEFAULT_TASK_PARAMS = {
        'bind': True,
        'autoretry_for': [
            Exception,
        ],
        'retry_kwargs': {'max_retries': 5},
        'retry_backoff': (1, 6),
        'retry_backoff_max': 5*60,
        'ignore_result': True,
        'acks_late': True,
    }
    ROUTES = {}
    QUEUE_NAME = None

    @classmethod
    def queue_prefix(cls):
        return '{config}.{proj}'.format(
            **cls.application.options['env']
        )

    @classmethod
    def queue_name(cls, name=None):
        if name:
            queue_name = name
        elif cls.QUEUE_NAME:
            queue_name = cls.QUEUE_NAME
        else:
            queue_name = inflection.underscore(cls.__name__)
        return '{queue_prefix}.{queue_name}'.format(
            queue_prefix=cls.queue_prefix(),
            queue_name=queue_name,
        )

    @classmethod
    def init(cls, application):
        cls.application = application
        cls.logger = logging.getLogger(cls.__name__)

    @classmethod
    def on_failure(cls, queue_name, autoretry):
        def __decorator(f):
            @wraps(f)
            def __wrapper(task, *args, **kwargs):
                try:
                    try:
                        return f(task, *args, **kwargs)
                    except (TaskPredicate, MaxRetriesExceededError):
                        raise
                    except Exception as e:
                        # If defined for autoretry, re-raise AutoRetryException
                        if autoretry['retry_backoff']:
                            countdown = int(random.uniform(*autoretry['retry_backoff']) ** (task.request.retries+1))
                            countdown = countdown if countdown < autoretry['retry_backoff_max'] \
                                else autoretry['retry_backoff_max']
                        else:
                            countdown = autoretry['retry_kwargs'].get('countdown', 0)
                        for need_retry_exp in autoretry['autoretry_for']:
                            if isinstance(e, need_retry_exp):
                                raise task.retry(exc=e, countdown=countdown, **autoretry['retry_kwargs'])
                        else:
                            raise
                except (TaskPredicate, MaxRetriesExceededError):
                    raise
                except Exception:
                    dl_prefix = cls.application.celery_app.conf.deadletter_prefix
                    dl_queue = dl_prefix + cls.queue_name(queue_name)
                    cls.logger.error(
                        'Send {task} to {eq}...'.format(
                            task = str(task),
                            eq = dl_queue
                        )
                    )
                    task.apply_async(args, kwargs, queue=dl_queue)
                    raise
            return __wrapper
        return __decorator
    
    @classmethod
    def check_rate_limiter(cls, f):
        @wraps(f)
        def __wrapper(task, *args, **kwargs):
            backoff = cls.application.options['rate-limiter']['backoff']
            backoff_max = cls.application.options['rate-limiter']['backoff_max']
            url = cls.application.options['rate-limiter']['url']
            rate_limiter_url = '{host}/{queue_name}'.format(
                host=url, queue_name=cls.queue_name()
            )
            r = requests.get(rate_limiter_url)
            
            countdown = int(random.uniform(*backoff) ** (task.request.retries+1))
            countdown = countdown if countdown < backoff_max else backoff_max
            if r.status_code != requests.codes.ok:
                cls.logger.warning('Exceed rate limit, will retry...')
                task.max_retries = None
                raise task.retry(countdown=countdown)
            else:
                task.max_retries = 3
            return f(task, *args, **kwargs)
        return __wrapper
    
    @classmethod
    def bind_func(cls, f, task_route=None, queue_name=None, **kwargs):
        task_name = '{queue_name}.{func_name}'.format(
            queue_name=cls.queue_name(queue_name),
            func_name=f.__name__,
        )
        default_kwargs = dict(cls.DEFAULT_TASK_PARAMS)
        default_kwargs['name'] = task_name
        default_kwargs.update(kwargs)
        # Hack autoretry decorator to exclude TaskPredicate exceptions
        autoretry = {
            'autoretry_for': default_kwargs.pop('autoretry_for', []),
            'retry_kwargs': default_kwargs.pop('retry_kwargs', []),
            'retry_backoff': default_kwargs.pop('retry_backoff', []),
            'retry_backoff_max': default_kwargs.pop('retry_backoff_max', None),
        }

        celery_task_deco = cls.application.celery_app.task(**default_kwargs)
        if task_route is None:
            cls.ROUTES[task_name] = {'queue': cls.queue_name(queue_name)}
        else:
            cls.ROUTES[task_name] = task_route
        # Applying decorators
        return celery_task_deco(
            cls.on_failure(queue_name=queue_name,
                           autoretry=autoretry)(
                cls.check_rate_limiter(f),
            )
        )

class AbstractCronTaskFactory(AbstractAsyncTaskFactory):
    QUEUE_NAME = 'default_cron_task_queue'
    DEFAULT_TASK_PARAMS = {
        'bind': True,
        'ignore_result': False,
    }
