from django.http import JsonResponse
from .models import *
    
def getUsers(request):
    usuaris = User.objects.filter(pk=request.user.pk)    
    jsonData = list(usuaris.values())
    return JsonResponse({
            "status": "OK",
            "UsersObj": jsonData,
        }, safe=False)