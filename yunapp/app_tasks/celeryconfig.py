# -*- coding: utf-8 -*-
# Celery configuration file
BROKER_URL = 'amqp://guest@localhost//'
CELERY_RESULT_BACKEND = 'amqp://guest@localhost//'

CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_RESULT_EXPIRES = 3600

CELERY_IMPORTS = ("yunapp.app_tasks.cel_tasks",)