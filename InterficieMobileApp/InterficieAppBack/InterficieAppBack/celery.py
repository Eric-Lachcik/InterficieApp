import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'InterficieAppBack.settings')
app = Celery('InterficieAppBack')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# Configuración para usar Redis como broker
app.conf.update(
    broker_url='redis://localhost:6379/0',
    result_backend='redis://localhost:6379/0',
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='Europe/Madrid',
    enable_utc=True,
)