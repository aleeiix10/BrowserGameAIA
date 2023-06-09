from django import forms
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.auth.decorators import login_required
from .models import *
from django.core.mail import send_mail
from .utils import *
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import CustomUserCreationForm
from django.utils import timezone
import datetime
from django.conf import settings
from .decorators import *
import random
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

@login_required
def profile(request):
    return render(request,"browserGame/profile.html")

@cronDecorator
def pagina_inicio(request):
    if request.user.is_authenticated:
        actions= Action.objects.all()
        userLoged = Event.objects.filter(user=request.user).order_by('-timestamp')[:25]
        form = UserAttackedForm(request.POST)
        level_range = [request.user.level-1, request.user.level, request.user.level+1]
        form.fields['jugador_a_atacar'].queryset = User.objects.filter(level__in=level_range).exclude(pk=request.user.pk)
        return render(request, 'browserGame/profile.html', {'userLoged': userLoged, "actions":actions, "form":form})
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

@cronDecorator
def play_action(request):
    if request.user.is_authenticated:
        user = request.user
        form = ActionForm(user, request.POST)
        profileAjaxActions(request)
        return render(request, 'browserGame/play_action.html', {'form': form})

    else:
        return render(request, 'browserGame/403.html', {}, status=403)

def play(user, action_used,random_numbers ,user_attacked=""):
    user_experience_after_action= 0
    random_atack= 0
    random_numbers= []
    #Si el coste de mana es mayor al mana actual del usuario, dará un error
    if action_used.cost > user.current_mana:
        msg= """
            <div id="alert-border-4" class="flex p-4 mb-4 text-yellow-800 border-t-4 border-yellow-300 bg-yellow-50 dark:text-yellow-300 dark:bg-gray-800 dark:border-yellow-800" role="alert">
                <svg class="flex-shrink-0 w-5 h-5" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd"></path></svg>
                <div class="ml-3 text-sm font-medium">
                No tens suficient manà
                </div>
                <button type="button" class="btn-alert ml-auto -mx-1.5 -my-1.5 bg-yellow-50 text-yellow-500 rounded-lg focus:ring-2 focus:ring-yellow-400 p-1.5 hover:bg-yellow-200 inline-flex h-8 w-8 dark:bg-gray-800 dark:text-yellow-300 dark:hover:bg-gray-700" data-dismiss-target="#alert-border-4" aria-label="Close">
                <span class="sr-only">Dismiss</span>
                <svg aria-hidden="true" class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"></path></svg>
                </button>
            </div>
        """

    elif action_used.category=='D' and user.current_life >= user.level * 10:
        msg= """
            <div id="alert-border-4" class="flex p-4 mb-4 text-yellow-800 border-t-4 border-yellow-300 bg-yellow-50 dark:text-yellow-300 dark:bg-gray-800 dark:border-yellow-800" role="alert">
                <svg class="flex-shrink-0 w-5 h-5" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd"></path></svg>
                <div class="ml-3 text-sm font-medium">
                Tens la salut al màxim
                </div>
                <button type="button" class="btn-alert ml-auto -mx-1.5 -my-1.5 bg-yellow-50 text-yellow-500 rounded-lg focus:ring-2 focus:ring-yellow-400 p-1.5 hover:bg-yellow-200 inline-flex h-8 w-8 dark:bg-gray-800 dark:text-yellow-300 dark:hover:bg-gray-700" data-dismiss-target="#alert-border-4" aria-label="Close">
                <span class="sr-only">Dismiss</span>
                <svg aria-hidden="true" class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"></path></svg>
                </button>
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
        random_numbers.append(random_atack)
        #Si el random es mayor que el porcentaje ha fallado la acción
        if random_atack > action_used.succesPercentage:
            event.success= False
            msg= f"""
                    <div id="alert-border-2" class="flex p-4 mb-4 text-red-800 border-t-4 border-red-300 bg-red-50 dark:text-red-400 dark:bg-gray-800 dark:border-red-800" role="alert">
                        <svg class="flex-shrink-0 w-5 h-5" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd"></path></svg>
                        <div class="ml-3 text-sm font-medium">
                        La teva acció {action_used.name} ha sigut fallida
                        </div>
                        <button type="button" class="btn-alert ml-auto -mx-1.5 -my-1.5 bg-red-50 text-red-500 rounded-lg focus:ring-2 focus:ring-red-400 p-1.5 hover:bg-red-200 inline-flex h-8 w-8 dark:bg-gray-800 dark:text-red-400 dark:hover:bg-gray-700"  data-dismiss-target="#alert-border-2" aria-label="Close">
                        <span class="sr-only">Dismiss</span>
                        <svg aria-hidden="true" class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"></path></svg>
                        </button>
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
                    <div id="alert-border-3" class="flex p-4 mb-4 text-green-800 border-t-4 border-green-300 bg-green-50 dark:text-green-400 dark:bg-gray-800 dark:border-green-800" role="alert">
                        <svg class="flex-shrink-0 w-5 h-5" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd"></path></svg>
                        <div class="ml-3 text-sm font-medium">
                        <strong class="font-bold">¡Atac exitòs!</strong> Has obtingut {action_used.points} punts d'experiència.
                        </div>
                        <button type="button" class="btn-alert ml-auto -mx-1.5 -my-1.5 bg-green-50 text-green-500 rounded-lg focus:ring-2 focus:ring-green-400 p-1.5 hover:bg-green-200 inline-flex h-8 w-8 dark:bg-gray-800 dark:text-green-400 dark:hover:bg-gray-700"  data-dismiss-target="#alert-border-3" aria-label="Close">
                        <span class="sr-only">Dismiss</span>
                        <svg aria-hidden="true" class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"></path></svg>
                        </button>
                    </div>
                """

            elif action_used.category == "D":
                if user.current_life + action_used.cost > user.level * 10:
                    user.current_life = user.level * 10
                    # <strong class="font-bold">¡Curació exitosa!</strong>
                    msg= f"""
                    <div id="alert-border-3" class="flex p-4 mb-4 text-green-800 border-t-4 border-green-300 bg-green-50 dark:text-green-400 dark:bg-gray-800 dark:border-green-800" role="alert">
                        <svg class="flex-shrink-0 w-5 h-5" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd"></path></svg>
                        <div class="ml-3 text-sm font-medium">
                        <strong class="font-bold">¡Curació exitosa!</strong> Has obtingut {action_used.points} punts de salut. <strong class="font-bold">Has arribat a la salut màxima</strong>
                        </div>
                        <button type="button" class="ml-auto -mx-1.5 -my-1.5 bg-green-50 text-green-500 rounded-lg focus:ring-2 focus:ring-green-400 p-1.5 hover:bg-green-200 inline-flex h-8 w-8 dark:bg-gray-800 dark:text-green-400 dark:hover:bg-gray-700"  data-dismiss-target="#alert-border-3" aria-label="Close">
                        <span class="sr-only">Dismiss</span>
                        <svg aria-hidden="true" class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"></path></svg>
                        </button>
                    </div>
                    """
                else:
                    user.current_life += action_used.points
                    msg= f"""
                    <div id="alert-border-3" class="flex p-4 mb-4 text-green-800 border-t-4 border-green-300 bg-green-50 dark:text-green-400 dark:bg-gray-800 dark:border-green-800" role="alert">
                        <svg class="flex-shrink-0 w-5 h-5" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd"></path></svg>
                        <div class="ml-3 text-sm font-medium">
                        <strong class="font-bold">¡Curació exitosa!</strong> Has obtingut {action_used.points} punts de salut
                        </div>
                        <button type="button" class="btn-alert ml-auto -mx-1.5 -my-1.5 bg-green-50 text-green-500 rounded-lg focus:ring-2 focus:ring-green-400 p-1.5 hover:bg-green-200 inline-flex h-8 w-8 dark:bg-gray-800 dark:text-green-400 dark:hover:bg-gray-700"  data-dismiss-target="#alert-border-3" aria-label="Close">
                        <span class="sr-only">Dismiss</span>
                        <svg aria-hidden="true" class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"></path></svg>
                        </button>
                    </div>
                    """
                user.save()

            elif action_used.category == "N":
                user.experience += action_used.points
                user.save()
                msg= f"""
                    <div id="alert-border-3" class="flex p-4 mb-4 text-green-800 border-t-4 border-green-300 bg-green-50 dark:text-green-400 dark:bg-gray-800 dark:border-green-800" role="alert">
                        <svg class="flex-shrink-0 w-5 h-5" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd"></path></svg>
                        <div class="ml-3 text-sm font-medium">
                        Exit! Has obtingut {action_used.points} punts de experiencia
                        </div>
                        <button type="button" class="btn-alert ml-auto -mx-1.5 -my-1.5 bg-green-50 text-green-500 rounded-lg focus:ring-2 focus:ring-green-400 p-1.5 hover:bg-green-200 inline-flex h-8 w-8 dark:bg-gray-800 dark:text-green-400 dark:hover:bg-gray-700"  data-dismiss-target="#alert-border-3" aria-label="Close">
                        <span class="sr-only">Dismiss</span>
                        <svg aria-hidden="true" class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"></path></svg>
                        </button>
                    </div>
                """
            if user.experience > user.level * 10:
                levelUp= user.experience // (user.level * 10)
                experienceRest= user.experience % (user.level * 10)
                user.level += levelUp
                user.experience= experienceRest - 1
                user.save()
                msg+= f"""
                    <div id="alert-border-1" class="flex p-4 mb-4 text-blue-800 border-t-4 border-blue-300 bg-blue-50 dark:text-blue-400 dark:bg-gray-800 dark:border-blue-800" role="alert">
                        <svg class="flex-shrink-0 w-5 h-5" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd"></path></svg>
                        <div class="ml-3 text-sm font-medium">
                        Has arribat a nivel {user.level}
                        </div>
                        <button type="button" class="btn-alert ml-auto -mx-1.5 -my-1.5 bg-blue-50 text-blue-500 rounded-lg focus:ring-2 focus:ring-blue-400 p-1.5 hover:bg-blue-200 inline-flex h-8 w-8 dark:bg-gray-800 dark:text-blue-400 dark:hover:bg-gray-700" data-dismiss-target="#alert-border-1" aria-label="Close">
                        <span class="sr-only">Dismiss</span>
                        <svg aria-hidden="true" class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"></path></svg>
                        </button>
                    </div>
                """
        event.save()
    return JsonResponse(random_numbers, msg, safe=False)

@csrf_exempt
def profileAjaxActions(request):
    lvl= False
    user_experience_after_action= 0
    session= SessionStore(session_key=request.session.session_key)

    # Obtener la lista de números generados de la sesión
    random_numbers = session.get('random_numbers', [])
    current_time = session.get('current_time', [])
    arrayActionsConsole= session.get('arrayActionsConsole',[])
    arraySuccesConsole= session.get('arraySuccesConsole',[])
    if request.method == "POST":
        user= request.user
        action_id= request.POST.get("button_choice")
        action_used = Action.objects.get(id=action_id)
        user_attacked_id= request.POST.get("jugador_a_atacar")

        if user_attacked_id == None or user_attacked_id == "":
            user_attacked = ""
        else:
            user_attacked= User.objects.get(id=user_attacked_id)
        #Si el coste de mana es mayor al mana actual del usuario, dará un error
        if action_used.cost > user.current_mana:
            msg= """
                <div id="alert-border-4" class="flex p-4 mb-4 text-yellow-800 border-t-4 border-yellow-300 bg-yellow-50 dark:text-yellow-300 dark:bg-gray-800 dark:border-yellow-800" role="alert">
                    <svg class="flex-shrink-0 w-5 h-5" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd"></path></svg>
                    <div class="ml-3 text-sm font-medium">
                    No tens suficient manà
                    </div>
                    <button type="button" class="ml-auto -mx-1.5 -my-1.5 bg-yellow-50 text-yellow-500 rounded-lg focus:ring-2 focus:ring-yellow-400 p-1.5 hover:bg-yellow-200 inline-flex h-8 w-8 dark:bg-gray-800 dark:text-yellow-300 dark:hover:bg-gray-700" data-dismiss-target="#alert-border-4" aria-label="Close">
                    <span class="sr-only">Dismiss</span>
                    <svg aria-hidden="true" class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"></path></svg>
                    </button>
                </div>
            """
            return JsonResponse({"mensaje": "No hay mana"})

        elif action_used.category=='D' and user.current_life >= user.level * 10:
            msg= """
                <div id="alert-border-4" class="flex p-4 mb-4 text-yellow-800 border-t-4 border-yellow-300 bg-yellow-50 dark:text-yellow-300 dark:bg-gray-800 dark:border-yellow-800" role="alert">
                    <svg class="flex-shrink-0 w-5 h-5" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd"></path></svg>
                    <div class="ml-3 text-sm font-medium">
                    Tens la salut al màxim
                    </div>
                    <button type="button" class="ml-auto -mx-1.5 -my-1.5 bg-yellow-50 text-yellow-500 rounded-lg focus:ring-2 focus:ring-yellow-400 p-1.5 hover:bg-yellow-200 inline-flex h-8 w-8 dark:bg-gray-800 dark:text-yellow-300 dark:hover:bg-gray-700" data-dismiss-target="#alert-border-4" aria-label="Close">
                    <span class="sr-only">Dismiss</span>
                    <svg aria-hidden="true" class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"></path></svg>
                    </button>
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
            random_atack= random.randint(0, 100)
            random_numbers.append(random_atack)
            # Guardar la lista actualizada en la sesión
            session['random_numbers'] = random_numbers

            actionTime= timezone.now()
            actionTime= actionTime.strftime('%Y-%m-%dT%H:%M:%SZ')
            current_time.append(actionTime)
            session['current_time'] = current_time

            if random_atack > action_used.succesPercentage:
                event.success= False
                msg= f"""
                        <div id="alert-border-2" class="flex p-4 mb-4 text-red-800 border-t-4 border-red-300 bg-red-50 dark:text-red-400 dark:bg-gray-800 dark:border-red-800" role="alert">
                            <svg class="flex-shrink-0 w-5 h-5" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd"></path></svg>
                            <div class="ml-3 text-sm font-medium">
                            La teva acció {action_used.name} ha sigut fallida
                            </div>
                            <button type="button" class="ml-auto -mx-1.5 -my-1.5 bg-red-50 text-red-500 rounded-lg focus:ring-2 focus:ring-red-400 p-1.5 hover:bg-red-200 inline-flex h-8 w-8 dark:bg-gray-800 dark:text-red-400 dark:hover:bg-gray-700"  data-dismiss-target="#alert-border-2" aria-label="Close">
                            <span class="sr-only">Dismiss</span>
                            <svg aria-hidden="true" class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"></path></svg>
                            </button>
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
                        <div id="alert-border-3" class="flex p-4 mb-4 text-green-800 border-t-4 border-green-300 bg-green-50 dark:text-green-400 dark:bg-gray-800 dark:border-green-800" role="alert">
                            <svg class="flex-shrink-0 w-5 h-5" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd"></path></svg>
                            <div class="ml-3 text-sm font-medium">
                            <strong class="font-bold">¡Atac exitòs!</strong> Has obtingut {action_used.points} punts d'experiència.
                            </div>
                            <button type="button" class="ml-auto -mx-1.5 -my-1.5 bg-green-50 text-green-500 rounded-lg focus:ring-2 focus:ring-green-400 p-1.5 hover:bg-green-200 inline-flex h-8 w-8 dark:bg-gray-800 dark:text-green-400 dark:hover:bg-gray-700"  data-dismiss-target="#alert-border-3" aria-label="Close">
                            <span class="sr-only">Dismiss</span>
                            <svg aria-hidden="true" class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"></path></svg>
                            </button>
                        </div>
                    """

                elif action_used.category == "D":
                    if user.current_life + action_used.cost > user.level * 10:
                        user.current_life = user.level * 10
                        msg= f"""
                        <div id="alert-border-3" class="flex p-4 mb-4 text-green-800 border-t-4 border-green-300 bg-green-50 dark:text-green-400 dark:bg-gray-800 dark:border-green-800" role="alert">
                            <svg class="flex-shrink-0 w-5 h-5" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd"></path></svg>
                            <div class="ml-3 text-sm font-medium">
                            <strong class="font-bold">¡Curació exitosa!</strong> Has obtingut {action_used.points} punts de salut. <strong class="font-bold">Has arribat a la salut màxima</strong>
                            </div>
                            <button type="button" class="ml-auto -mx-1.5 -my-1.5 bg-green-50 text-green-500 rounded-lg focus:ring-2 focus:ring-green-400 p-1.5 hover:bg-green-200 inline-flex h-8 w-8 dark:bg-gray-800 dark:text-green-400 dark:hover:bg-gray-700"  data-dismiss-target="#alert-border-3" aria-label="Close">
                            <span class="sr-only">Dismiss</span>
                            <svg aria-hidden="true" class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"></path></svg>
                            </button>
                        </div>
                        """
                    else:
                        user.current_life += action_used.points
                        msg= f"""
                        <div id="alert-border-3" class="flex p-4 mb-4 text-green-800 border-t-4 border-green-300 bg-green-50 dark:text-green-400 dark:bg-gray-800 dark:border-green-800" role="alert">
                            <svg class="flex-shrink-0 w-5 h-5" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd"></path></svg>
                            <div class="ml-3 text-sm font-medium">
                            <strong class="font-bold">¡Curació exitosa!</strong> Has obtingut {action_used.points} punts de salut
                            </div>
                            <button type="button" class="ml-auto -mx-1.5 -my-1.5 bg-green-50 text-green-500 rounded-lg focus:ring-2 focus:ring-green-400 p-1.5 hover:bg-green-200 inline-flex h-8 w-8 dark:bg-gray-800 dark:text-green-400 dark:hover:bg-gray-700"  data-dismiss-target="#alert-border-3" aria-label="Close">
                            <span class="sr-only">Dismiss</span>
                            <svg aria-hidden="true" class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"></path></svg>
                            </button>
                        </div>
                        """
                    user.save()

                elif action_used.category == "N":
                    user.experience += action_used.points
                    user.save()
                    msg= f"""
                        <div id="alert-border-3" class="flex p-4 mb-4 text-green-800 border-t-4 border-green-300 bg-green-50 dark:text-green-400 dark:bg-gray-800 dark:border-green-800" role="alert">
                            <svg class="flex-shrink-0 w-5 h-5" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd"></path></svg>
                            <div class="ml-3 text-sm font-medium">
                            Exit! Has obtingut {action_used.points} punts de experiencia
                            </div>
                            <button type="button" class="ml-auto -mx-1.5 -my-1.5 bg-green-50 text-green-500 rounded-lg focus:ring-2 focus:ring-green-400 p-1.5 hover:bg-green-200 inline-flex h-8 w-8 dark:bg-gray-800 dark:text-green-400 dark:hover:bg-gray-700"  data-dismiss-target="#alert-border-3" aria-label="Close">
                            <span class="sr-only">Dismiss</span>
                            <svg aria-hidden="true" class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"></path></svg>
                            </button>
                        </div>
                    """
                
                if user.experience > user.level * 10:
                    levelUp= user.experience // (user.level * 10)
                    experienceRest= user.experience % (user.level * 10)
                    user.level += levelUp
                    user.experience= experienceRest - 1
                    user.save()
                    lvl= True
                    msg+= f"""
                        <div id="alert-border-1" class="flex p-4 mb-4 text-blue-800 border-t-4 border-blue-300 bg-blue-50 dark:text-blue-400 dark:bg-gray-800 dark:border-blue-800" role="alert">
                            <svg class="flex-shrink-0 w-5 h-5" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd"></path></svg>
                            <div class="ml-3 text-sm font-medium">
                            Has arribat a nivel {user.level}
                            </div>
                            <button type="button" class="ml-auto -mx-1.5 -my-1.5 bg-blue-50 text-blue-500 rounded-lg focus:ring-2 focus:ring-blue-400 p-1.5 hover:bg-blue-200 inline-flex h-8 w-8 dark:bg-gray-800 dark:text-blue-400 dark:hover:bg-gray-700" data-dismiss-target="#alert-border-1" aria-label="Close">
                            <span class="sr-only">Dismiss</span>
                            <svg aria-hidden="true" class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"></path></svg>
                            </button>
                        </div>
                    """
            
            actionUsedConsole= Action.objects.filter(id=action_id).values("name", "succesPercentage")
            actionUsedConsole= list(actionUsedConsole)
            arrayActionsConsole.append(actionUsedConsole)
            session['arrayActionsConsole']= arrayActionsConsole

            arraySuccesConsole.append(event.success)
            session["arraySuccesConsole"]= arraySuccesConsole
            session.save()
            event.save()
        return JsonResponse({"mensaje": "Los datos se han guardado correctamente Play 2",
                             "lvl":lvl,
                             "arrayAction": arrayActionsConsole, 
                             "arrayRandom": random_numbers, 
                             "arrayTime":current_time, 
                             "arraySuccess":arraySuccesConsole})

    else:
        return JsonResponse({
                            "arrayAction": arrayActionsConsole, 
                            "arrayRandom": random_numbers, 
                            "arrayTime":current_time, 
                            "arraySuccess":arraySuccesConsole
        })

def ranking(request, username=None):
    if username:
        user = User.objects.filter(username=username)
        if user:
            return render(request, 'browserGame/profileRanking.html', {'username': username})
        else:
            return render(request, 'browserGame/404.html', status=404)
    else:
        if request.user.is_authenticated:
            users= User.objects.all().order_by('-level', '-experience','-current_life','-current_mana')
            return render(request, 'browserGame/logedRanking.html', {'users':users})
        else:
            users= User.objects.all().order_by('-level', '-experience','-current_life','-current_mana')
            return render(request, 'browserGame/generalRanking.html', {'users':users})

def actions(request):
    if request.user.is_authenticated:
        return render(request, 'browserGame/logedActions.html')
    else:
        return render(request,'browserGame/generalActions.html')


#CLASES
class UserAttackedForm(forms.Form):
    jugador_a_atacar = forms.ModelChoiceField(queryset=User.objects.all())

class ActionForm(forms.Form):
    button_choice = forms.ModelChoiceField(queryset=Action.objects.all())
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
        self.fields['button_choice'].choices = options

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
