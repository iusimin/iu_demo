SERVICE_CONFIG = {
    'server': [
        'run',
        '--use-aliases', '--service-ports', '--rm',
        'demo',
    ],
    'fe-shell': [
        'run',
        '--use-aliases', '--service-ports', '--rm',
        'fe-shell', 'sh'
    ],
    'nginx-reload': [
        'exec',
        'nginx', '/bin/bash'#'service', 'nginx', 'reload',
    ],
    'worker': [
        'run',
        '--use-aliases', '--service-ports', '--rm',
        'demo-worker', 'python', 'worker.py', # Need input
    ],
    'worker-shell': [
        'run',
        '--use-aliases', '--service-ports', '--rm',
        'demo-worker', '/bin/bash',
    ],
    'redis-shell': [
        'run',
        '--use-aliases', '--service-ports', '--rm',
        'redis', '/bin/bash',
    ],
    'infra': [
        'up',
        '--abort-on-container-exit',
        'nginx', 'mongodb', 'mongo-express', 'rabbitmq', 'celery-flower', 'rate-limiter', 'redis'
    ],
    'rate-limiter-config': [
        'exec', 'rate-limiter',
        'python3', 'cli.py', 'manage',
    ],
}