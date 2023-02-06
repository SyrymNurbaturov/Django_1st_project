from django.apps import AppConfig

class PollsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'polls'

from django.apps import AppConfig
from django.core.signals import request_finished

from django.dispatch import receiver

@receiver(request_finished)
def my_callback(sender, **kwargs):
    print("Request finished!")

class MyAppConfig(AppConfig):


    def ready(self):
        from . import signals
        request_finished.connect(signals.my_callback)