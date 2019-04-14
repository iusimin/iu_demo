SERVICE_CONFIG = {
    'vue-frontend-server': [
        'run',
        '--use-aliases', '--service-ports', '--rm',
        'vue-frontend',
    ],
    'server': [
        'run',
        '--use-aliases', '--service-ports', '--rm',
        'wms',
    ],
    'infra': [
        'up',
        '--abort-on-container-exit',
        'nginx', 'mongodb', 'mongo-express', 'rabbitmq', 'celery-flower', 'rate-limiter', 'redis'
    ]
}