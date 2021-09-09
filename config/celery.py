import os
import django
from datetime import timedelta


from celery import Celery
from django.conf import settings



os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')


django.setup()

app = Celery('config')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)



# scheduler

app.conf.beat_schedule = {
    'remind-users-to-activate-account': {
        'task':'apps.core.tasks.remind_users_to_activate_code',
        'schedule':timedelta(days=1) # everyday
    },

}





@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))

