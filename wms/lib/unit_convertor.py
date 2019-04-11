"""Extract the unit from text
"""

def memory_to_kb(memory_str):
    FACTOR = {
        'KB': 1,
        'MB': 1024,
        'GB': 1024*1024,
        'TB': 1024*1024*1024,
        'PB': 1024*1024*1024*1024,
    }
    try:
        value, unit = memory_str[:-2], memory_str[-2:]
        value = int(value) * FACTOR[unit.upper()]
    except Exception:
        raise ValueError('Invalid memory format %s' % memory_str)
    return value

def time_to_second(time_str):
    FACTOR = {
        'S': 1,
        'M': 60,
        'H': 3600,
        'D': 3600*24,
    }
    try:
        value, unit = time_str[:-1], time_str[-1:]
        value = int(value) * FACTOR[unit.upper()]
    except Exception:
        raise ValueError('Invalid time format %s' % time_str)
    return value