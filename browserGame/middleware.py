from datetime import datetime
from django.contrib.auth import get_user
from .models import Log
from .utils import log_eventU

class LogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.user.is_authenticated:
            user = get_user(request)
            log_eventU(user,'I',"Se h'accedit a la ruta " + str(request.path))

        return response