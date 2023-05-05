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

@cronDecorator
def play_action(request):
    if request.user.is_authenticated:
        form = ActionForm()
        if request.method == "POST":
            form = ActionForm(request.POST)
            if form.is_valid():
                user = request.user
                atack_used = form.cleaned_data.get('acció')
                atacked_user = form.cleaned_data.get('jugador_a_atacar')
                #si el coste de mana es mayor al mana que tiene error
                if atack_used.cost > user.current_mana:
                    print(form.errors)
                #si tiene el mana suficiente para atacar
                else: 
                    random_atack = random.randint(0, 100)
                    #si el random es mayor que el porcentaje ha fallado el ataque
                    if random_atack > atack_used.succesPercentage:
                        user.current_mana -= atack_used.cost
                        user.save()
                        #ha fallado el ataque
                        print(form.errors)
                    #si no falla el ataque
                    else:
                        user.current_mana -= atack_used.cost
                        user.experience = user_experience_before_atack
                        user_experience_before_atack = user.experience + atack_used.cost
                        if user_experience_before_atack > user.level*10:
                            user.level += 1
                            user.save()
                        life_before_atack = atacked_user.current_life - atack_used.points
                        if life_before_atack > user.max_life:



                        
        level_range = [request.user.level-1, request.user.level, request.user.level+1]
        form.fields['jugador_a_atacar'].queryset = User.objects.filter(level__in=level_range).exclude(pk=request.user.pk)
        return render(request, 'browserGame/play_action.html', {'form': form, })

    else:
        return render(request, 'browserGame/403.html', {}, status=403)
