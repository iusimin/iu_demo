SERVICE_CONFIG = {
    'server': [
        'run',
        '--use-aliases', '--service-ports', '--rm',
        'wms',
    ],
    'worker': [
        'run',
        '--use-aliases', '--service-ports', '--rm',
        'wms-worker', 'python', 'worker.py', # Need input
    ],
    'infra': [
        'up',
        '--abort-on-container-exit',
        'nginx', 'mongodb', 'mongo-express', 'rabbitmq', 'celery-flower', 'rate-limiter', 'redis'
    ]
}