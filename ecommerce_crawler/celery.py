# ecommerce_crawler/celery.py

import os
from celery import Celery

# Set default settings module for the 'celery' program
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_crawler.settings')

celery_app = Celery('ecommerce_crawler')

# Load task modules from all registered Django app configs.
celery_app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks in installed Django apps
celery_app.autodiscover_tasks()

@celery_app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
