import os
from celery import Celery
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.settings")

app = Celery('tasks', broker=settings.RABBITMQ_URL)