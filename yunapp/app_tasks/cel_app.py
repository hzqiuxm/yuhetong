from celery import Celery
from yunapp.app_tasks import celeryconfig
cel_app = Celery()
cel_app.config_from_object(celeryconfig)

if __name__ == '__main__':
    cel_app.start()