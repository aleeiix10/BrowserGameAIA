from .models import *
#from django.contrib.auth.models import User

#Guarda en el modelo Log informacion del typo, el usuario y el mensaje
def systemLogU(user, typeLog, message):
    log = Log(user=user, typeLog=typeLog, message=message)
    log.save()

#Es el modelo del Cron para sumar +1 de mana
def cronManaU():
    users= User.objects.all()
    for user in users:
        if user.current_mana < user.level * 10 and user.level > 0:
            user.current_mana +=1
            user.save()