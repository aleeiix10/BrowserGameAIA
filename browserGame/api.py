from django.http import JsonResponse
from .models import *
 
def get_user(request):
    jsonData = list(User.objects.all().order_by('-level', '-experience','-current_life','-current_mana').values(
        'username', 'level', 'experience','current_life', 'current_mana'
        ))
    return JsonResponse({
            "status": "OK",
            "users": jsonData,
        }, safe=False)