from django import forms
from django.shortcuts import render
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import *
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import send_mail
from .models import *
from .utils import *
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from .forms import CustomUserCreationForm
from django.utils import timezone
import datetime
from django.contrib.auth.decorators import login_required
from .models import *
from .utils import *
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from .decorators import *
import random

    
@login_required
def profile(request):
    return render(request,"browserGame/profile.html")


def index(request):
    context = {}
    return render(request, 'browserGame/index.html', context)

#@login_required
#def writeLog(request):
#    return render(request, 'browserGame/index.html')
@cronDecorator
def pagina_inicio(request):
    if request.user.is_authenticated:
        userLoged = Event.objects.filter(user=request.user).order_by('-timestamp')[:30]
        return render(request, 'browserGame/profile.html', {'userLoged': userLoged, })
    else:
        now = timezone.now()
        global_option = GlobalOption.objects.first()
        time_left = global_option.end_date - now
        time_left_str = str(time_left - datetime.timedelta(microseconds=time_left.microseconds))
        context = {
            'global_option': global_option,
            'time_left': time_left_str,
        }
        return render(request, 'browserGame/index.html', context)

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            send_mail(
                'Benvingut a la meva aplicació',
                'Hola {0}, gràcies per registrar-te en la meva aplicació.'.format(user.username),
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False,
            )
            return redirect('/')
        else:
            print(form.errors)
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

class ActionForm(forms.Form):
    acció = forms.ModelChoiceField(Action.objects.all())
    jugador_a_atacar = forms.ModelChoiceField(queryset=None)

