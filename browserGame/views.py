from django.shortcuts import render
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .utils import *

def index(request):
    context = {}
    return render(request, 'browserGame/index.html', context)

@login_required
def writeLog(request):
    systemLog(User.objects.get(id=2), 'I', 'El usuario ha iniciado sesión')
    return render(request, 'browserGame/index.html')