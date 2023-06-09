from .utils import *
from django.utils import timezone
from .models import *
def cronDecorator(function):
    def wrapper(request, *args, **kwargs):
        crontime = GlobalOption.objects.first()
        response = function(request, *args, **kwargs)
        # Ejecutar la función después de que se carga la vista
        cron = GlobalOption.objects.first()
        time_since_last_run = timezone.now() - cron.last_updated_cron
        if time_since_last_run.seconds >= crontime.time_cron_execute_seconds:
            mana= time_since_last_run.seconds//crontime.time_cron_execute_seconds
            cronManaU(mana)
        return response
    return wrapper