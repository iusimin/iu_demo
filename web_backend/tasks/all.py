from web_backend.tasks.sample_light import SampleLightTasks
from web_backend.tasks.sample_heavy import SampleHeavyTasks
from web_backend.tasks.crons.test_cron_task import SampleCronTask

ALL = [
    SampleLightTasks,
    SampleHeavyTasks,
]
CRONS = [
    SampleCronTask,
]