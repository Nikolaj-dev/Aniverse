from celery import Celery
import os


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aniverse.settings')


app = Celery('aniverse')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

