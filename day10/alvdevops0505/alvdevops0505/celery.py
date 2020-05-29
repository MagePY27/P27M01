import os
from celery import Celery, platforms
import django
from django.conf import settings

# set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "alvdevops0505.settings")

django.setup()

app = Celery('devops')
platforms.C_FORCE_ROOT = True
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))