from wms.tasks.sample_light import SampleLightTasks
from wms.tasks.sample_heavy import SampleHeavyTasks

ALL = [
    SampleLightTasks,
    SampleHeavyTasks,
]
ALL_NAME = [
    t.__name__ for t in ALL
]