from wms_backend.tasks.sample_light import SampleLightTasks
from wms_backend.tasks.sample_heavy import SampleHeavyTasks

ALL = [
    SampleLightTasks,
    SampleHeavyTasks,
]
ALL_NAME = [
    t.__name__ for t in ALL
]