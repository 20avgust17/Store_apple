import os
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'shop.settings')

app = Celery('shop')
app.config_from_object('django.conf:settings', namespace="CELERY")
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'every-1-minute': {
        'task': 'store.tasks.send_spam_email',
        'schedule': crontab(0, 0, day_of_month='1-7,15-21'),

    }
}
