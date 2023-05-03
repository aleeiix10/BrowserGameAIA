from .utils import *
from django.utils import timezone

def cronDecorator(function):
    def wrapper(request, *args, **kwargs):
        response = function(request, *args, **kwargs)
        # Ejecutar la función después de que se carga la vista
        cron = GlobalOption.objects.first()
        time_since_last_run = timezone.now() - cron.last_updated_cron
        if time_since_last_run.seconds >= 3600:
            mana= time_since_last_run.seconds//3600
            cronManaU(mana)
        return response
    return wrapper