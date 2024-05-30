import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
app = Celery('accounts')
app.config_from_object('django.conf:settings')
broker_connection_retry = False

app.autodiscover_tasks()