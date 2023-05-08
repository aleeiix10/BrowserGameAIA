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

@cronDecorator
def pagina_inicio(request):
    if request.user.is_authenticated:
        userLoged = Event.objects.filter(user=request.user).order_by('-timestamp')[:25]
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
    action = forms.ModelChoiceField(queryset=Action.objects.all())
    jugador_a_atacar = forms.ModelChoiceField(queryset=User.objects.all(),required=False)

    def __init__(self, user,*args, **kwargs):
        super().__init__(*args, **kwargs)
        action_queryset = Action.objects.all()
        options = [(None, '--------')]
        for category, label in Action.categories:
            group = (label, [])
            for action in action_queryset.filter(category=category, cost__lte=user.current_mana):
                #Incluir el name y succesPercentage en la etiqueta de la opción
                label = f"{action.name} ({action.succesPercentage}%) - {action.cost}"
                group[1].append((action.id, label))
            if group[1]:
                options.append(group)
        self.fields['action'].choices = options

        allowed_levels = [user.level - 1, user.level, user.level + 1]
        user_queryset = User.objects.filter(level__in=allowed_levels).exclude(pk=user.pk)
        options = [ (None, '--------') ]
        for user in user_queryset:
            if user.level == 0:
                continue
            label = f"{user.username} (Nivel {user.level})"
            options.append((user.id, label))
        self.fields['jugador_a_atacar'].choices = options

    def clean(self):
        cleaned_data = super().clean()
        action = cleaned_data.get('action')
        jugador_a_atacar = cleaned_data.get('jugador_a_atacar')
        
        if action and action.category == 'A' and not jugador_a_atacar:
            self.add_error('jugador_a_atacar', 'Este campo es obligatorio para acciones agresivas.')

@cronDecorator
def play_action(request):
    msg= ""
    user_experience_after_action= 0
    lvl= ""
    if request.user.is_authenticated:
        user = request.user
        form = ActionForm(user, request.POST)
        if request.method == "POST":
            if form.is_valid():
                action_used = form.cleaned_data.get('action') #ATAQUE USADO DEL JUGADOR
                user_attacked = form.cleaned_data.get('jugador_a_atacar') #JUGADOR ATACADO

                #Si el coste de mana es mayor al mana actual del usuario, dará un error
                if action_used.cost > user.current_mana:
                    msg= """
                        <div class="container mx-auto my-4 bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative" role="alert">
                            <strong class="font-bold">¡Error!</strong>
                            <span class="block sm:inline">No tens suficient manà</span>
                        </div>
                    """

                elif action_used.category=='D' and user.current_life >= user.level * 10:
                    msg= """
                        <div class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative" role="alert">
                            <strong class="font-bold">¡Error!</strong>
                            <span class="block sm:inline">Tens la salut al màxim</span>
                        </div>
                    """

                #Sí tiene el mana suficiente para atacar
                else: 
                    user.current_mana -= action_used.cost
                    user.save()

                    event= Event()
                    event.action= action_used
                    event.user= user

                    #Vemos si ha acertado el la accion
                    random_atack = random.randint(0, 100)
                    #Si el random es mayor que el porcentaje ha fallado la acción
                    if random_atack > action_used.succesPercentage:
                        event.success= False
                        msg= """
                                <div class="container mx-auto my-4 bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative" role="alert">
                                    <strong class="font-bold">¡Error!</strong>
                                    <span class="block sm:inline">Tu acció ha fallat</span>
                                </div>
                            """
                        if action_used.category=="A":
                            event.user_attacked= user_attacked
                    #Si acierta el ataque
                    else:
                        event.success= True
                        if action_used.category == "A":
                            event.user_attacked= user_attacked

                            #Experiencia extra si el jugador atacado muere
                            if (user_attacked.current_life - action_used.points) <= 0:

                                #Número aleatori entre el nivell del jugador atacant i el nivell del jugador víctima x 2.
                                if user.level > user_attacked.level:
                                    randomNum = random.randint(user_attacked.level,user.level)
                                else:
                                    randomNum = random.randint(user.level, user_attacked.level)

                                user_experience_after_action = (user.experience + action_used.points) + (randomNum * 2)

                                #Saber si al jugador atacado lo hemos matado del todo
                                if user_attacked.level - 1 == 0:
                                    user_attacked.level= 0
                                    user_attacked.current_life= 0
                                    user_attacked.current_mana= 0
                                    user_attacked.experience= 0
                                
                                else:
                                    user_attacked.level-= 1
                                    user_attacked.current_life= (user_attacked.level) * 10

                                    if user_attacked.current_mana > (user_attacked.level) * 10:
                                        user_attacked.current_mana= (user_attacked.level)*10

                                    if user_attacked.experience > (user_attacked.level) * 10:
                                        user_attacked.experience= (user_attacked.level)*10
                            #Ataque Normal, solo le bajamos la vida
                            else:
                                user_experience_after_action= user.experience + action_used.points
                                user_attacked.current_life -= action_used.points

                            user_attacked.save()
                            user.experience= user_experience_after_action
                            user.save()
                            msg= f"""
                                <div class="container mx-auto my-4 bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded relative" role="alert">
                                    <strong class="font-bold">Atac exitòs!</strong>
                                    <span class="block sm:inline">Has obtingut {action_used.points} punts d'experiencia</span>
                                </div>
                            """

                        elif action_used.category == "D":
                            if user.current_life + action_used.cost > user.level * 10:
                                user.current_life = user.level * 10
                                msg= f"""
                                <div class="container mx-auto my-4 bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded relative" role="alert">
                                    <strong class="font-bold">¡Curació exitosa!</strong>
                                    <span class="block sm:inline">Has obtingut {action_used.points} punts de salut. Tens el màxim de salut</span>
                                </div>
                                """
                            else:
                                user.current_life += action_used.points
                                msg= f"""
                                <div class="container mx-auto my-4 bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded relative" role="alert">
                                    <strong class="font-bold">¡Curació exitosa!</strong>
                                    <span class="block sm:inline">Has obtingut {action_used.points} punts de salut</span>
                                </div>
                                """
                            user.save()

                        elif action_used.category == "N":
                            user.experience += action_used.points
                            user.save()
                            msg= f"""
                                <div class="container mx-auto my-4 bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded relative" role="alert">
                                    <strong class="font-bold">¡Éxit!</strong>
                                    <span class="block sm:inline">Has obtingut {action_used.points} punts d'experiencia</span>
                                </div>
                            """
                        if user.experience > user.level * 10:
                            levelUp= user.experience // (user.level * 10)
                            print("LEVEL UP: " + str(levelUp))
                            experienceRest= user.experience % (user.level * 10)
                            print("EXP REST: " + str(experienceRest))
                            user.level += levelUp
                            user.experience= experienceRest - 1
                            user.save()
                            lvl= f"""
                                <div class="bg-blue-100 border border-blue-400 text-blue-700 px-4 py-3 rounded relative" role="alert">
                                    <strong class="font-bold">Informació!</strong>
                                    <span class="block sm:inline">Has augmentad de nivel a {user.level}</span>
                                    <span class="absolute top-0 bottom-0 right-0 px-4 py-3">
                                        <svg class="fill-current h-6 w-6 text-blue-500" role="button" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"><title>Close</title><path d="M14.348 5.652a.999.999 0 1 0-1.414 1.414L11 8.414l-1.935 1.934a.999.999 0 1 0 1.414 1.414L12.414 10l1.934 1.935a.999.999 0 1 0 1.414-1.414L13.828 10l1.935-1.935a.999.999 0 0 0 0-1.414z"/></svg>
                                    </span>
                                </div>
                            """
                    event.save()
        return render(request, 'browserGame/play_action.html', {'form': form, 'msg':msg, 'lvl':lvl})

    else:
        return render(request, 'browserGame/403.html', {}, status=403)
