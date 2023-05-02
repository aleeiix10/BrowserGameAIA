from .models import *


def systemLog(user, typeLog, message):
    log = Log(user=user, typeLog=typeLog, message=message)
    log.save()