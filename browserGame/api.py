from django.http import JsonResponse
from .models import *
from django.db.models import Q 
from itertools import chain
from .decorators import cronDecorator

def get_user(request):
    jsonData = list(User.objects.exclude(level=0).order_by('-level', '-experience','-current_life','-current_mana').values(
        'username', 'level', 'experience','current_life', 'current_mana'
        ))
    return JsonResponse({
            "status": "OK",
            "users": jsonData,
        }, safe=False)

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


def getActions(request):
    actions = Action.objects.all()
    jsonData = list(actions.values())
    return JsonResponse({
        "status": "OK",
        "ActionsObj": jsonData,
    }, safe=False)


def getUsersByName(request, username):
    user = User.objects.filter(username=username)
    userSelected = User.objects.filter(username=username).first()
    getRelatedEvents = Event.objects.filter(user=userSelected)
    jsonData = list(user.values())
    jsonData2 = list(getRelatedEvents.values())
    return JsonResponse({
        "status": "OK",
        "userObj": jsonData,
        "actionObj" : jsonData2
    }, safe=False)
