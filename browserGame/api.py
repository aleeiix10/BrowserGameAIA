from django.http import JsonResponse
from .models import *
from django.db.models import Q 
from itertools import chain
from .decorators import cronDecorator

@cronDecorator
def getUsers(request):
    usuaris = User.objects.filter(pk=request.user.pk)    
    jsonData = list(usuaris.values())
    return JsonResponse({
            "status": "OK",
            "UsersObj": jsonData,
        }, safe=False)


@cronDecorator
def getRelatedActions(request):
    events = Event.objects.filter(Q(user = request.user) | (Q(user_attacked = request.user,success = True))).order_by('-timestamp').values('user__username','user_attacked__username','action__name','action__category','timestamp','action__cost','action__points','success')[:25]
    jsonData = list(events)
    return JsonResponse({
        "status": "OK",
        "ActionsObj": jsonData,
    }, safe=False)
