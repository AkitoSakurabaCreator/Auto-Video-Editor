# import os

# from celery import Celery

# Set the default Django settings module for the 'celery' program.
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")

# Celery app作成
# project名, brokerのホストを指定
# app = Celery("mysite", broker="redis://localhost:6379/1")
# app.conf.result_backend = "redis://localhost:6379/1"


# from __future__ import absolute_import, unicode_literals

# import os

# from celery import Celery

# set the default Django settings module for the 'celery' program.
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

# app = Celery('mysite')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
# app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
# app.autodiscover_tasks()


# @app.task(bind=True)
# def debug_task(self):
#     print('Request: {0!r}'.format(self.request))


# celery.py
# from __future__ import absolute_import, unicode_literals

# import os

# from celery import Celery

# set the default Django settings module for the 'celery' program.
# os.environ.setdefault(
#     'DJANGO_SETTINGS_MODULE',
#     'mysite.settings'
# )

# app = Celery('mysite') 

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
# app.config_from_object(
#     'django.conf:settings',
#     namespace='CELERY'
# )

# Load task modules from all registered Django app configs.
# app.autodiscover_tasks()


# @app.task(bind=True)
# def debug_task(self):
#     print('Request: {0!r}'.format(self.request))




from __future__ import absolute_import, unicode_literals

import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

app = Celery('mysite')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

# from .tasks import add, Edit
@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
