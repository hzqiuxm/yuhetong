from celery import Celery

cel_app = Celery('cel_app',
             broker='amqp://guest@localhost//',
             backend='amqp://guest@localhost//',
             include=['app_tasks.cel_tasks'])

# Optional configuration, see the application user guide.
cel_app.conf.update(
    CELERY_TASK_RESULT_EXPIRES=3600,
)

if __name__ == '__main__':
    cel_app.start()