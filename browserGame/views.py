from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import *
from .utils import *
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from .decorators import *

@cronDecorator
def pagina_inicio(request):
    if request.user.is_authenticated:
        return render(request, 'browserGame/index_protected.html')
    else:
        return render(request, 'browserGame/index.html')
         
@login_required
def profile(request):
    return render(request,"browserGame/profile.html")

def enviar_email(request):
    template = render_to_string('browserGame/email_template.html', {'user': 'Andres'})

    email = EmailMessage(
        'Bienvenido a BrowserGame',
        template,
        settings.EMAIL_HOST_USER,
        ['evillcatunari.cf@iesesteveterradas.cat']
    )

    email.fail_silently = False
    email.send()  

    return  render(request, 'browserGame/email_sent.html')

def index(request):
    context = {}
    return render(request, 'browserGame/index.html', context)

@login_required
def writeLog(request):
    log_eventU(request.user, 'I', 'El usuario ha iniciado sesión')
    return render(request, 'browserGame/index.html')