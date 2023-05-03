from .models import *

from django.core.cache import cache
import datetime
from django.utils import timezone

#Guarda en el modelo Log informacion del typo, el usuario y el mensaje
def systemLogU(log_entries):
    log_objects = [Log(typeLog=e['type'], message=e['msg'], user=e['user'], created_at=e['timestamp']) for e in log_entries]
    Log.objects.bulk_create(log_objects)

def log_eventU(event_user, event_type, event_msg):
    log_entry = {
        'type': event_type,
        'msg': event_msg,
        'user': event_user,
        'timestamp': datetime.datetime.now(),
    }
    log_entries = cache.get('log_entries')
    if log_entries is None:
        log_entries = []
    log_entries.append(log_entry)
    if len(log_entries) >= 5:
        # Escribir los registros en la base de datos
        systemLogU(log_entries)
        log_entries = []
    cache.set('log_entries', log_entries)

#Es el modelo del Cron para sumar +1 de mana
def cronManaU(mana):
    users= User.objects.all()

    for i in range(mana):
        for user in users:
            if user.current_mana < user.level * 10 and user.level > 0:
                user.current_mana += user.level
                if user.level * 10 < user.current_mana:
                    user.current_mana = user.level * 10
                user.save()

    cron = GlobalOption.objects.first()
    cron.last_updated_cron = timezone.now()
    cron.save()