import os

from celery import Celery

# Set default Django settings module for Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hse_task.settings')

app = Celery('hse_task')

# Load config from Django settings, using a namespace
app.config_from_object('django.conf:settings', namespace='CELERY')

# Autodiscover tasks from all installed Django apps
app.autodiscover_tasks()
