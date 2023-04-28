from .models import *
#from django.contrib.auth.models import User

def systemLog(user, typeLog, message):
    log = Log(user=user, typeLog=typeLog, message=message)
    log.save()