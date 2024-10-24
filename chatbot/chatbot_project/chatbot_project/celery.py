from __future__ import absolute_import, unicode_literals
import os 
from celery import celery
from django.conf import settings


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chatbot_prject.settings')

app=Celery('chatbot_project')
app.conf.enable_utc=False

app.conf.update(timezone= 'Asia/Kolkata')

app.config_from_object(settings,namespace='CELERY')

#Celery Beat Settings

app.autodiscovertasks_tasks()

@app.task(bind=True)

def debug_task(self):
    print(f"Request : {self.request!r}")